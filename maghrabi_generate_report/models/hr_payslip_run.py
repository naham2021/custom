from odoo import fields, models, api, _
import xlsxwriter
from io import BytesIO
import base64
from datetime import datetime


class HrPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'

    report = fields.Binary(string='Download', readonly=True)
    report_name = fields.Char()

    def employee_fields(self):
        # generate termination values and suspensions values for employees
        # if  the employee have a suspension and termination requests dirng the batch period
        # add them as a text in termination and sustension fields in employee model just to appear in batch report

        # { 'key': ('column_order', 'column_name') }
        employee_fields = {
            'attendance_id': ('0', 'Attendance ID'),
            'old_id': ('1', 'Old Emp ID'),
            'name': ('2', 'Name'),
            'gender': ('3', 'Gender'),
            'department_id.name': ('4', 'Department'),
            'job_id.name': ('5', 'Position'),
            'assignment_number': ('6', 'Assignment Number'),
            'bank_account_number': ('7', 'Account Number'),
            'organisation.name': ('8', 'Organisation Name'),
            'contract_id.bank_wage': ('9', 'Bank Wage'),
            'bank_id.name': ('10', 'Bank'),
            'payment_method': ('11', 'Payment Method'),
            'contract_id.wage': ('12', 'Wage'),
            'contract_id.basic_salary': ('13', 'Basic'),
            'contract_id.cash_wage': ('14', 'Cash Wage'),
            'contract_id.fixed_other_allowance': ('15', 'Fixed Other Allowance'),
            'contract_id.fixed_transportation_allowance': ('16', 'Fixed Transportation Allowance'),
            'contract_id.natural_allowance': ('17', 'Nature Allowance'),
            'contract_id.previous_special_bonus': ('18', 'Previous Special Bonus'),
            'contract_id.special_bonus': ('19', 'Special Bonus'),
            'terminations': ('20', 'Terminations'),
            'suspensions': ('21', 'suspensions'),
        }
        return employee_fields

    def _fetch_data(self):
        data = []
        employee_fields = self.employee_fields()

        for payslip in self.slip_ids:
            row = {}
            employee_contract = self.env['hr.contract'].search([
                ('employee_id', '=', payslip.employee_id.id),
                ('state', '=', 'open')])

            for idx, field in enumerate(employee_fields):
                object = payslip.employee_id
                names = field.split('.')

                for name in names:
                    object = getattr(object, name, 'NULL')

                value = object if object else 'NULL'
                row.update({'%s_%s' % (employee_fields[field][0], employee_fields[field][1]): value})

            salary_rules = {}
            for line in payslip.line_ids:
                salary_rules.update({str(line.salary_rule_id.id): line.amount})
                if line.category_id.name == 'Basic':
                    row.update({'9999_Basic diff': line.amount - line.total})

            row.update({'salary_rules': salary_rules})
            print(row)
            data.append(row)

        return data

    def _combine_data_to_salary_rules(self, data):
        salary_rules = self.env['hr.salary.rule'].search([])

        # :labels: Contains all salary rules defined in the system.
        labels = {}
        for sal in salary_rules:
            labels.update({str(sal.id): {'name': sal.name, 'code': sal.code, 'sequence': sal.sequence + 100}})

        # :result: key -> Column name, value -> Column's rows.
        result = {}
        for key in data[0]:
            if not key == 'salary_rules':
                result.update({key: ['NULL'] * len(data)})
        for l in labels:
            result.update({l: ['NULL'] * len(data)})

        for idx, row in enumerate(data):
            for key in row:
                if key == 'salary_rules':
                    for k in row[key]:
                        if k in labels:
                            result[k][idx] = row[key][k]
                else:
                    result[key][idx] = row[key]

        # :new_result: Changed :result columns names.
        new_result = {}

        for key in result:
            if key in labels:
                new_result.update({'%s_%s' % (labels[key]['sequence'], labels[key]['name']): result[key]})
            else:
                new_result.update({key: result[key]})

        return new_result

    def _write_to_excel_file(self, new_result, data):
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})

        font_size_10 = workbook.add_format(
            {'font_name': 'KacstBook', 'font_size': 10, 'align': 'center', 'valign': 'vcenter',  # 'text_wrap': True,
             'border': 1})

        table_header_formate = workbook.add_format({
            'bold': 1,
            'border': 1,
            'bg_color': '#AAB7B8',
            'font_size': '10',
            'align': 'center',
            'valign': 'vcenter',
            'text_wrap': True
        })

        sheet = workbook.add_worksheet('Payslips Report')
        sheet.set_column(0, len(new_result), 40)
        sheet.set_row(0, 20)

        for key in new_result:
            col = new_result[key]
            sum = 0
            for it in col:
                if type(it) == int or type(it) == float:
                    sum += it
            col.append(sum if sum else '')
        # Writing to the excel sheet.
        ordered_keys = sorted([(int(it.split('_')[0]), it) for it in new_result.keys()], key=lambda x: x[0])
        for idx, key in enumerate(ordered_keys):
            sheet.write(0, idx, key[1].split('_')[1] if len(key[1].split('_')) > 1 else key[1], table_header_formate)
            for row_idx in range(1, len(data) + 2):
                sheet.write(row_idx, idx, new_result[key[1]][row_idx - 1], table_header_formate if row_idx == len(data) + 1 else font_size_10)

        workbook.close()
        output.seek(0)
        self.report = base64.encodestring(output.read())
        self.report_name = 'payslips' + str(datetime.today().strftime('%Y-%m-%d')) + '.xlsx'

    @api.one
    def generate_excel(self):
        """
        Create report and export it into excel file.

        TODO improve loops complexities, try avoid using ORM and use RAW SQL instead to improve performance.
        """

        # :data: List of rows of the report.
        data = self._fetch_data()
        new_result = self._combine_data_to_salary_rules(data)
        self._write_to_excel_file(new_result, data)
        return {
            "type": "ir.actions.do_nothing",
        }

    def close_payslip_run(self):
        res = super(HrPayslipRun, self).close_payslip_run()
        for slip in self.slip_ids:
            slip.action_payslip_done()
        return res

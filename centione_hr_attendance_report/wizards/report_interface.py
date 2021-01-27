from odoo import models, fields, api, _
from datetime import datetime, timedelta
import itertools


class ReportInterface(models.TransientModel):
    _name = 'report.interface'

    report_type = fields.Selection([('0', 'Absence'), ('1', 'Late & Early'), ('2', 'Attendance')])
    date_from = fields.Date()
    date_to = fields.Date()
    group_by = fields.Selection([('0', 'By Employee'),
                                ('1', 'By Company'),
                                ('2', 'By Department')])
    filter_by = fields.Selection([('0', 'Employees'),
                                  ('1', 'Company'),
                                  ('2', 'Department')])
    employee_ids = fields.Many2many('hr.employee')
    company_ids = fields.Many2many('res.company')
    department_ids = fields.Many2many('hr.department')

    def _report_writer(self, report_name=None, date_from=None, date_to=None, table_header=None, table_data=None):
        report_title = _('''%(report_name)s Report FROM %(date_from)s TO %(date_to)s''') % {
            'report_name': report_name,
            'date_from': str(date_from),
            'date_to': str(date_to)
        }
        if table_data is None:
            table_data = [[]]
        if table_header is None:
            table_header = []
        pdf = self.env.ref('centione_hr_attendance_report.action_report_absence_report').render_qweb_pdf(
            data={'report_name': report_title, 'date_from': date_from, 'date_to': date_to, 'table_header': table_header, 'table_data': table_data})
        return pdf[0]

    def _absence_report(self, group_by=None, date_from=None, date_to=None, filter_by=None, filter_ids=None):
        conditions = [('date', '<=', datetime.strptime(str(date_to), '%Y-%m-%d').date()),
                      ('date', '>=', datetime.strptime(str(date_from), '%Y-%m-%d').date())]

        if filter_by == '0':
            conditions.append(('employee_id', 'in', filter_ids))
        elif filter_by == '1':
            conditions.append(('employee_id.company_id', 'in', filter_ids))
        elif filter_by == '2':
            conditions.append(('employee_id.department_id', 'in', filter_ids))


        raw_data = [(it.employee_id.name, it.employee_id.company_id.name, it.employee_id.department_id.name, it.date)
                    for it in self.env['hr.absence'].search(conditions)]

        if group_by == '0':
            table_header = [_('Employee'), _('Absence Count')]
            an_iterator = itertools.groupby(sorted(raw_data, key=lambda x: str(x[0])), lambda x: str(x[0]))
            aggregated_data = [(i, len(list(j))) for i, j in an_iterator]
            table_data = aggregated_data
        elif group_by == '1':
            table_header = [_('Company'), _('Absence Count')]
            an_iterator = itertools.groupby(sorted(raw_data, key=lambda x: str(x[1])), lambda x: str(x[1]))
            aggregated_data = [(i, len(list(j))) for i, j in an_iterator]
            table_data = aggregated_data
        elif group_by == '2':
            table_header = [_('Department'), _('Absence Count')]
            an_iterator = itertools.groupby(sorted(raw_data, key=lambda x: str(x[2])), lambda x: str(x[2]))
            aggregated_data = [(i, len(list(j))) for i, j in an_iterator]
            table_data = aggregated_data
        else:
            table_header = [_('Employee'), _('Company'), _('Department'), _('Date')]
            table_data = raw_data

        report_name = _("Absence")
        pdf = self._report_writer(report_name=report_name,
                                  date_from=date_from,
                                  date_to=date_to,
                                  table_header=table_header,
                                  table_data=table_data)
        return pdf

    def _late_early_report(self, group_by=None, date_from=None, date_to=None, filter_by=None, filter_ids=None):
        print("Late Early Report")
        conditions = [('check_in', '<=', datetime.strptime(str(date_to), '%Y-%m-%d') + timedelta(hours=23, minutes=59, seconds=59)),
                      ('check_in', '>=', datetime.strptime(str(date_from), '%Y-%m-%d')),
                      '|', ('late_attendance_hours', '>', 0), ('early_leave_hours', '>', 0)]

        if filter_by == '0':
            conditions.append(('employee_id', 'in', filter_ids))
        elif filter_by == '1':
            conditions.append(('employee_id.company_id', 'in', filter_ids))
        elif filter_by == '2':
            conditions.append(('employee_id.department_id', 'in', filter_ids))

        raw_data = [(it.employee_id.name, it.employee_id.company_id.name, it.employee_id.department_id.name,
                     it.check_in.date(), it.late_attendance_hours, it.early_leave_hours)
                    for it in self.env['hr.attendance'].search(conditions)]

        f2time = lambda f: '{0:02.0f}:{1:02.0f}'.format(*divmod(f * 60, 60))
        if group_by == '0':
            table_header = [_('Employee'), _('Days Count'), _('Total Late'), _('Total Early')]
            an_iterator = itertools.groupby(sorted(raw_data, key=lambda x: str(x[0])), lambda x: str(x[0]))
            aggregated_data = [(i, list(j)) for i, j in an_iterator]
            table_data = [(it[0], len(it[1]), f2time(sum([i[4] for i in it[1]])), f2time(sum([i[5] for i in it[1]])))
                          for it in aggregated_data]
        elif group_by == '1':
            table_header = [_('Company'), _('Days Count'), _('Total Late'), _('Total Early')]
            an_iterator = itertools.groupby(sorted(raw_data, key=lambda x: str(x[1])), lambda x: str(x[1]))
            aggregated_data = [(i, list(j)) for i, j in an_iterator]
            table_data = [(it[0], len(it[1]), f2time(sum([i[4] for i in it[1]])), f2time(sum([i[5] for i in it[1]])))
                          for it in aggregated_data]
        elif group_by == '2':
            table_header = [_('Department'), _('Days Count'), _('Total Late'), _('Total Early')]
            an_iterator = itertools.groupby(sorted(raw_data, key=lambda x: str(x[2])), lambda x: str(x[2]))
            aggregated_data = [(i, list(j)) for i, j in an_iterator]
            table_data = [(it[0], len(it[1]), f2time(sum([i[4] for i in it[1]])), f2time(sum([i[5] for i in it[1]])))
                          for it in aggregated_data]
        else:
            table_header = [_('Employee'), _('Company'), _('Department'), _('Date'), _('Late Hours'), _('Early Hours')]
            raw_data = [it[:4] + (f2time(it[4]), f2time(it[5])) for it in raw_data]
            table_data = raw_data

        report_name = _("Lateness & Earliness")
        pdf = self._report_writer(report_name=report_name,
                                  date_from=date_from,
                                  date_to=date_to,
                                  table_header=table_header,
                                  table_data=table_data)
        return pdf

    def _attendance_report(self, group_by=None, date_from=None, date_to=None, filter_by=None, filter_ids=None):
        conditions = [('check_in', '<=', datetime.strptime(str(date_to), '%Y-%m-%d') + timedelta(hours=23, minutes=59, seconds=59)),
                      ('check_in', '>=', datetime.strptime(str(date_from), '%Y-%m-%d'))]

        if filter_by == '0':
            conditions.append(('employee_id', 'in', filter_ids))
        elif filter_by == '1':
            conditions.append(('employee_id.company_id', 'in', filter_ids))
        elif filter_by == '2':
            conditions.append(('employee_id.department_id', 'in', filter_ids))

        raw_data = [(it.employee_id.name, it.employee_id.company_id.name, it.employee_id.department_id.name,
                     it.check_in, it.check_out)
                    for it in self.env['hr.attendance'].search(conditions)]

        if group_by == '0':
            table_header = [_('Employee'), _('Days Count')]
            an_iterator = itertools.groupby(sorted(raw_data, key=lambda x: str(x[0])), lambda x: str(x[0]))
            aggregated_data = [(i, len(list(j))) for i, j in an_iterator]
            table_data = aggregated_data
        elif group_by == '1':
            table_header = [_('Company'), _('Days Count')]
            an_iterator = itertools.groupby(sorted(raw_data, key=lambda x: str(x[1])), lambda x: str(x[1]))
            aggregated_data = [(i, len(list(j))) for i, j in an_iterator]
            table_data = aggregated_data
        elif group_by == '2':
            table_header = [_('Department'), _('Days Count')]
            an_iterator = itertools.groupby(sorted(raw_data, key=lambda x: str(x[2])), lambda x: str(x[2]))
            aggregated_data = [(i, len(list(j))) for i, j in an_iterator]
            table_data = aggregated_data
        else:
            table_header = [_('Employee'), _('Company'), _('Department'), _('Check In'), _('Check Out')]
            table_data = raw_data

        report_name = _("Attendance")
        pdf = self._report_writer(report_name=report_name,
                                  date_from=date_from,
                                  date_to=date_to,
                                  table_header=table_header,
                                  table_data=table_data)
        return pdf


    def context(self):
        return {
            '0': self._absence_report,
            '1': self._late_early_report,
            '2': self._attendance_report
        }

    def get_report(self):
        path = "/attendance_report?"
        filter_by = filter_ids = None
        if self.filter_by == '0':
            filter_by = self.filter_by
            filter_ids = self.employee_ids.ids
        elif self.filter_by == '1':
            filter_by = self.filter_by
            filter_ids = self.company_ids.ids
        elif self.filter_by == '2':
            filter_by = self.filter_by
            filter_ids = self.department_ids.ids

        url = path + "report_type={}&group_by={}&date_from={}&date_to={}".\
            format(self.report_type, self.group_by, self.date_from, self.date_to)

        if filter_by:
            url += "&filter_by={}&filter_ids={}".format(filter_by, filter_ids)

        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
            'tag': 'reload',
        }

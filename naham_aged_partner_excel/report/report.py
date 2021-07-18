import time
from odoo import api, models, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero
from datetime import datetime
from dateutil.relativedelta import relativedelta


class PartnerXlsx(models.AbstractModel):
    _name = 'report.naham_aged_partner_excel.report_agedpartnerbalance'
    _inherit = 'report.report_xlsx.abstract'

    def _get_partner_move_lines(self, account_type, date_from, target_move, period_length, partners_filter=[]):
        # This method can receive the context key 'include_nullified_amount' {Boolean}
        # Do an invoice and a payment and unreconcile. The amount will be nullified
        # By default, the partner wouldn't appear in this report.
        # The context key allow it to appear
        # In case of a period_length of 30 days as of 2019-02-08, we want the following periods:
        # Name       Stop         Start
        # 1 - 30   : 2019-02-07 - 2019-01-09
        # 31 - 60  : 2019-01-08 - 2018-12-10
        # 61 - 90  : 2018-12-09 - 2018-11-10
        # 91 - 120 : 2018-11-09 - 2018-10-11
        # +120     : 2018-10-10
        print('first')
        periods = {}
        start = datetime.strptime(date_from, "%Y-%m-%d")
        date_from = datetime.strptime(date_from, "%Y-%m-%d").date()
        for i in range(5)[::-1]:
            stop = start - relativedelta(days=period_length)
            period_name = str((5-(i+1)) * period_length + 1) + '-' + str((5-i) * period_length)
            period_stop = (start - relativedelta(days=1)).strftime('%Y-%m-%d')
            if i == 0:
                period_name = '+' + str(4 * period_length)
            periods[str(i)] = {
                'name': period_name,
                'stop': period_stop,
                'start': (i!=0 and stop.strftime('%Y-%m-%d') or False),
            }
            start = stop
        print('second')
        res = []
        total = []
        cr = self.env.cr
        user_company = self.env.user.company_id
        user_currency = user_company.currency_id
        ResCurrency = self.env['res.currency'].with_context(date=date_from)
        company_ids = self._context.get('company_ids') or [user_company.id]
        move_state = ['draft', 'posted']
        if target_move == 'posted':
            move_state = ['posted']
        arg_list = (tuple(move_state), tuple(account_type))
        #build the reconciliation clause to see what partner needs to be printed
        reconciliation_clause = '(l.reconciled IS FALSE)'
        cr.execute('SELECT debit_move_id, credit_move_id FROM account_partial_reconcile where max_date > %s', (date_from,))
        reconciled_after_date = []
        for row in cr.fetchall():
            reconciled_after_date += [row[0], row[1]]
        if reconciled_after_date:
            reconciliation_clause = '(l.reconciled IS FALSE OR l.id IN %s)'
            arg_list += (tuple(reconciled_after_date),)
        arg_list += (date_from, tuple(company_ids))
        query = '''
            SELECT DISTINCT l.partner_id, UPPER(res_partner.name)
            FROM account_move_line AS l left join res_partner on l.partner_id = res_partner.id, account_account, account_move am
            WHERE (l.account_id = account_account.id)
                AND (l.move_id = am.id)
                AND (am.state IN %s)
                AND (account_account.internal_type IN %s)
                AND ''' + reconciliation_clause + '''
                AND (l.date <= %s)
                AND l.company_id IN %s
            ORDER BY UPPER(res_partner.name)'''
        cr.execute(query, arg_list)
        print('third')

        partners = cr.dictfetchall()

        if partners_filter:
            partners = [partner for partner in partners if partner['partner_id'] in partners_filter]

        print('---------------------------------------------')
        print('partners_filter',partners_filter)
        print('partners',partners)
        # put a total of 0
        for i in range(7):
            total.append(0)

        # Build a string like (1,2,3) for easy use in SQL query
        partner_ids = [partner['partner_id'] for partner in partners if partner['partner_id']]
        lines = dict((partner['partner_id'] or False, []) for partner in partners)
        if not partner_ids:
            return [], [], {}

        # This dictionary will store the not due amount of all partners
        undue_amounts = {}
        query = '''SELECT l.id
                FROM account_move_line AS l, account_account, account_move am
                WHERE (l.account_id = account_account.id) AND (l.move_id = am.id)
                    AND (am.state IN %s)
                    AND (account_account.internal_type IN %s)
                    AND (COALESCE(l.date_maturity,l.date) >= %s)\
                    AND ((l.partner_id IN %s) OR (l.partner_id IS NULL))
                AND (l.date <= %s)
                AND l.company_id IN %s'''
        print('fourth')
        cr.execute(query, (tuple(move_state), tuple(account_type), date_from, tuple(partner_ids), date_from, tuple(company_ids)))
        aml_ids = cr.fetchall()
        aml_ids = aml_ids and [x[0] for x in aml_ids] or []
        for line in self.env['account.move.line'].browse(aml_ids):
            partner_id = line.partner_id.id or False
            if partner_id not in undue_amounts:
                undue_amounts[partner_id] = 0.0
            line_amount = ResCurrency._compute(line.company_id.currency_id, user_currency, line.balance)
            if user_currency.is_zero(line_amount):
                continue
            for partial_line in line.matched_debit_ids:
                if partial_line.max_date <= date_from:
                    line_amount += ResCurrency._compute(partial_line.company_id.currency_id, user_currency, partial_line.amount)
            for partial_line in line.matched_credit_ids:
                if partial_line.max_date <= date_from:
                    line_amount -= ResCurrency._compute(partial_line.company_id.currency_id, user_currency, partial_line.amount)
            if not self.env.user.company_id.currency_id.is_zero(line_amount):
                undue_amounts[partner_id] += line_amount
                lines.get(partner_id, []).append({
                    'line': line,
                    'amount': line_amount,
                    'period': 6,
                })

        # Use one query per period and store results in history (a list variable)
        # Each history will contain: history[1] = {'<partner_id>': <partner_debit-credit>}
        print('fivth')
        history = []
        for i in range(5):
            args_list = (tuple(move_state), tuple(account_type), tuple(partner_ids),)
            dates_query = '(COALESCE(l.date_maturity,l.date)'

            if periods[str(i)]['start'] and periods[str(i)]['stop']:
                dates_query += ' BETWEEN %s AND %s)'
                args_list += (periods[str(i)]['start'], periods[str(i)]['stop'])
            elif periods[str(i)]['start']:
                dates_query += ' >= %s)'
                args_list += (periods[str(i)]['start'],)
            else:
                dates_query += ' <= %s)'
                args_list += (periods[str(i)]['stop'],)
            args_list += (date_from, tuple(company_ids))

            query = '''SELECT l.id
                    FROM account_move_line AS l, account_account, account_move am
                    WHERE (l.account_id = account_account.id) AND (l.move_id = am.id)
                        AND (am.state IN %s)
                        AND (account_account.internal_type IN %s)
                        AND ((l.partner_id IN %s) OR (l.partner_id IS NULL))
                        AND ''' + dates_query + '''
                    AND (l.date <= %s)
                    AND l.company_id IN %s'''
            print('sixth')
            cr.execute(query, args_list)
            partners_amount = {}
            aml_ids = cr.fetchall()
            aml_ids = aml_ids and [x[0] for x in aml_ids] or []
            for line in self.env['account.move.line'].browse(aml_ids):
                partner_id = line.partner_id.id or False
                if partner_id not in partners_amount:
                    partners_amount[partner_id] = 0.0
                line_amount = ResCurrency._compute(line.company_id.currency_id, user_currency, line.balance)
                if user_currency.is_zero(line_amount):
                    continue
                for partial_line in line.matched_debit_ids:
                    if partial_line.max_date <= date_from:
                        line_amount += ResCurrency._compute(partial_line.company_id.currency_id, user_currency, partial_line.amount)
                for partial_line in line.matched_credit_ids:
                    if partial_line.max_date <= date_from:
                        line_amount -= ResCurrency._compute(partial_line.company_id.currency_id, user_currency, partial_line.amount)

                if not self.env.user.company_id.currency_id.is_zero(line_amount):
                    partners_amount[partner_id] += line_amount
                    lines.get(partner_id, []).append({
                        'line': line,
                        'amount': line_amount,
                        'period': i + 1,
                        })
            history.append(partners_amount)

        print('siventh')


        for partner in partners:
            if partner['partner_id'] is None:
                partner['partner_id'] = False
            at_least_one_amount = False
            values = {}
            undue_amt = 0.0
            if partner['partner_id'] in undue_amounts:  # Making sure this partner actually was found by the query
                undue_amt = undue_amounts[partner['partner_id']]

            total[6] = total[6] + undue_amt
            values['direction'] = undue_amt
            if not float_is_zero(values['direction'], precision_rounding=self.env.user.company_id.currency_id.rounding):
                at_least_one_amount = True

            for i in range(5):
                during = False
                if partner['partner_id'] in history[i]:
                    during = [history[i][partner['partner_id']]]
                # Adding counter
                total[(i)] = total[(i)] + (during and during[0] or 0)
                values[str(i)] = during and during[0] or 0.0
                if not float_is_zero(values[str(i)], precision_rounding=self.env.user.company_id.currency_id.rounding):
                    at_least_one_amount = True
            values['total'] = sum([values['direction']] + [values[str(i)] for i in range(5)])
            ## Add for total
            total[(i + 1)] += values['total']
            values['partner_id'] = partner['partner_id']
            if partner['partner_id']:
                browsed_partner = self.env['res.partner'].browse(partner['partner_id'])
                values['name'] = browsed_partner.name and len(browsed_partner.name) >= 60 and browsed_partner.name[0:60] + '...' or browsed_partner.name
                values['trust'] = browsed_partner.trust
            else:
                values['name'] = _('Unknown Partner')
                values['trust'] = False

            if at_least_one_amount or (self._context.get('include_nullified_amount') and lines[partner['partner_id']]):
                res.append(values)

        return res, total, lines


    def generate_xlsx_report(self, workbook, data, partners):
        if not data.get('form') or not self.env.context.get('active_model') or not self.env.context.get('active_id'):
            raise UserError(_("Form content is missing, this report cannot be printed."))

        total = []
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))

        target_move = data['form'].get('target_move', 'all')
        date_from = data['form'].get('date_from', time.strftime('%Y-%m-%d'))

        if data['form']['result_selection'] == 'customer':
            account_type = ['receivable']
        elif data['form']['result_selection'] == 'supplier':
            account_type = ['payable']
        else:
            account_type = ['payable', 'receivable']

        movelines, total, dummy = self._get_partner_move_lines(account_type, date_from, target_move,
                                                               data['form']['period_length'],
                                                               data['form']['partner_ids'])


        # return {
        #     'doc_ids': self.ids,
        #     'doc_model': model,
        #     'data': data['form'],
        #     'docs': docs,
        #     'time': time,
        #     'get_partner_lines': movelines,
        #     'get_direction': total,
        # }


        sheet = workbook.add_worksheet('data')
        fromat1 = workbook.add_format({'font_name': 'KacstBook','border': 2, 'font_size': 14, 'align': 'vcenter', 'bold': True,'bg_color': '#a9a9a9'})
        fromat2 = workbook.add_format({'border': 1, 'font_size': 10, 'align': 'vcenter'})
        fromat3 = workbook.add_format({'border': 1, 'font_size': 10, 'align': 'vcenter', 'bold': True,'bg_color': '#AAB7B8','text_wrap':False})

        sheet.set_column(0, 0, 45)
        sheet.set_column(7, 7, 15)
        sheet.write('A1', 'Partners', fromat1)
        sheet.write('B1', 'not due', fromat1)
        sheet.write('C1', data['form']['4']['name'], fromat1)
        sheet.write('D1', data['form']['3']['name'], fromat1)
        sheet.write('E1', data['form']['2']['name'], fromat1)
        sheet.write('F1', data['form']['1']['name'], fromat1)
        sheet.write('G1', data['form']['0']['name'], fromat1)
        sheet.write('H1', 'Total', fromat1)

        if movelines:
           sheet.write(1, 0, 'Account Total', fromat3)
           sheet.write(1, 1, str(round(total[6],2))+'SR', fromat3)
           sheet.write(1, 2, str(round(total[4],2))+'SR', fromat3)
           sheet.write(1, 3, str(round(total[3],2))+'SR', fromat3)
           sheet.write(1, 4, str(round(total[2],2))+'SR', fromat3)
           sheet.write(1, 5, str(round(total[1],2))+'SR', fromat3)
           sheet.write(1, 6, str(round(total[0],2))+'SR', fromat3)
           sheet.write(1, 7, str(round(total[5],2))+'SR', fromat3)

        row = 2
        for partner in movelines:
            sheet.write(row, 0, partner['name'], fromat2)
            sheet.write(row, 1, str(round(partner['direction'],2))+"SR", fromat2)
            sheet.write(row, 2, str(round(partner['4'],2))+'SR', fromat2)
            sheet.write(row, 3, str(round(partner['3'],2))+'SR', fromat2)
            sheet.write(row, 4, str(round(partner['2'],2))+'SR', fromat2)
            sheet.write(row, 5, str(round(partner['1'],2))+'SR', fromat2)
            sheet.write(row, 6, str(round(partner['0'],2))+'SR', fromat2)
            sheet.write(row, 7, str(round(partner['total'],2))+'SR', fromat2)
            row += 1





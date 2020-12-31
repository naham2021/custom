# -*- coding: utf-8 -*-

from collections import defaultdict
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero


class ResPartner(models.Model):
    _inherit = 'pos.session'

    def _create_cash_statement_lines_and_cash_move_lines(self, data):
        # Create the split and combine cash statement lines and account move lines.
        # Keep the reference by statement for reconciliation.
        # `split_cash_statement_lines` maps `statement` -> split cash statement lines
        # `combine_cash_statement_lines` maps `statement` -> combine cash statement lines
        # `split_cash_receivable_lines` maps `statement` -> split cash receivable lines
        # `combine_cash_receivable_lines` maps `statement` -> combine cash receivable lines
        MoveLine = data.get('MoveLine')
        split_receivables_cash = data.get('split_receivables_cash')
        combine_receivables_cash = data.get('combine_receivables_cash')

        statements_by_journal_id = {statement.journal_id.id: statement for statement in self.statement_ids}
        print("statements_by_journal_id :: ",statements_by_journal_id)
        # handle split cash payments
        split_cash_statement_line_vals = defaultdict(list)
        split_cash_receivable_vals = defaultdict(list)
        for payment, amounts in split_receivables_cash.items():
            if payment.payment_method_id.receivable_account_id.id:
                is_partner = True
            print("statements_by_journal_id 22:: ", statements_by_journal_id)

            print("payment.payment_method_id.cash_journal_id.id",payment.payment_method_id.cash_journal_id.id)
            statement = statements_by_journal_id[payment.payment_method_id.cash_journal_id.id]
            print("statement :: ", statement)

            split_cash_statement_line_vals[statement].append(self._get_statement_line_vals(is_partner,payment,statement, payment.payment_method_id.receivable_account_id, amounts['amount'], payment.payment_date))
            line_vals = self._get_statement_line_vals(is_partner,payment,statement, payment.payment_method_id.receivable_account_id, amounts['amount'], payment.payment_date)
            # split_cash_statement_line_vals[statement].append(self._get_statement_line_vals(is_partner,payment,statement, payment.payment_method_id.receivable_account_id, amounts['amount']))

            split_cash_receivable_vals[statement].append(self._get_split_receivable_vals(payment, amounts['amount'], amounts['amount_converted']))
        # handle combine cash payments
        combine_cash_statement_line_vals = defaultdict(list)
        combine_cash_receivable_vals = defaultdict(list)
        for payment_method, amounts in combine_receivables_cash.items():
            if not float_is_zero(amounts['amount'] , precision_rounding=self.currency_id.rounding):
                statement = statements_by_journal_id[payment_method.cash_journal_id.id]
                combine_cash_statement_line_vals[statement].append(self._get_statement_line_vals(statement, payment_method.receivable_account_id, amounts['amount']))
                #             combine_cash_statement_line_vals[statement].append(self._get_statement_line_vals(statement, payment_method.receivable_account_id, amounts['amount']))
                combine_cash_receivable_vals[statement].append(self._get_combine_receivable_vals(payment_method, amounts['amount'], amounts['amount_converted']))
        # create the statement lines and account move lines
        BankStatementLine = self.env['account.bank.statement.line']
        split_cash_statement_lines = {}
        combine_cash_statement_lines = {}
        split_cash_receivable_lines = {}
        combine_cash_receivable_lines = {}
        # raise ValidationError(
        #     _("Show All Data ddd '%s'")
        #     % split_cash_receivable_vals[statement]
        # )

        account_custom = 0
        if split_cash_statement_line_vals:
            for s in split_cash_receivable_vals[statement]:
                partner = self.env['res.partner'].search([('id', '=', s['partner_id'])], limit=1)
                account_custom = 0
                if partner:
                    print("name partner :: ",partner.name)
                    print("partner.property_account_receivable_id.name 22222",partner.property_account_receivable_id.name)
                    account_custom = partner.property_account_receivable_id.id
                MoveLine.create({
                    'debit': s['credit'],
                    'credit': s['debit'],
                    'account_id': account_custom,
                    'move_id': s['move_id'],
                    'partner_id': s['partner_id'],
                     'name': 'Form Invoice'})
        for statement in self.statement_ids:
            split_cash_statement_lines[statement] = BankStatementLine.create(split_cash_statement_line_vals[statement])
            combine_cash_statement_lines[statement] = BankStatementLine.create(combine_cash_statement_line_vals[statement])
            split_cash_receivable_lines[statement] = MoveLine.create(split_cash_receivable_vals[statement])
            combine_cash_receivable_lines[statement] = MoveLine.create(combine_cash_receivable_vals[statement])

        data.update(
            {'split_cash_statement_lines':    split_cash_statement_lines,
             'combine_cash_statement_lines':  combine_cash_statement_lines,
             'split_cash_receivable_lines':   split_cash_receivable_lines,
             'combine_cash_receivable_lines': combine_cash_receivable_lines
             })

        return data

    def _create_invoice_receivable_lines(self, data):
        # Create invoice receivable lines for this session's move_id.
        # Keep reference of the invoice receivable lines because
        # they are reconciled with the lines in order_account_move_receivable_lines
        MoveLine = data.get('MoveLine')
        invoice_receivables = data.get('invoice_receivables')

        invoice_receivable_vals = defaultdict(list)
        invoice_receivable_lines = {}
        for receivable_account_id, amounts in invoice_receivables.items():
            invoice_receivable_vals[receivable_account_id].append(self._get_invoice_receivable_vals(receivable_account_id, amounts['amount'], amounts['amount_converted']))
        # for receivable_account_id, vals in invoice_receivable_vals.items():
        #     receivable_line = MoveLine.create(vals)
        #     if (not receivable_line.reconciled):
        #         invoice_receivable_lines[receivable_account_id] = receivable_line

        data.update({'invoice_receivable_lines': invoice_receivable_lines})
        return data


    def _get_statement_line_vals(self,is_partner,payment, statement, receivable_account, amount, date=False):
        print('receivable_account.id',receivable_account.id)
        print('_get_statement_line_vals')
        print('is_partner', is_partner)
        if is_partner == True:
            print("payment.partner_id",payment.partner_id)
            print("payment.partner_id.id",payment.partner_id.id)
            id = self.env['res.partner'].search([('id', '=', payment.partner_id.id)], limit=1).id

            # id = self.env["res.partner"]._find_accounting_partner(payment.partner_id).id
        return {
            'date': fields.Date.context_today(self, timestamp=date),
            'amount': amount,
            'name': self.name,
            'partner_id': id,
            'statement_id': statement.id,
            'account_id': receivable_account.id,
        }


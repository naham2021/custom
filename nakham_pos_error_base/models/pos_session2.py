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

    # def _create_account_move(self):
    #     """ Create account.move and account.move.line records for this session.
    #
    #     Side-effects include:
    #         - setting self.move_id to the created account.move record
    #         - creating and validating account.bank.statement for cash payments
    #         - reconciling cash receivable lines, invoice receivable lines and stock output lines
    #     """
    #     journal = self.config_id.journal_id
    #     # Passing default_journal_id for the calculation of default currency of account move
    #     # See _get_default_currency in the account/account_move.py.
    #     account_move = self.env['account.move'].with_context(default_journal_id=journal.id).create({
    #         'journal_id': journal.id,
    #         'date': fields.Date.context_today(self),
    #         'ref': self.name,
    #     })
    #     self.write({'move_id': account_move.id})
    #
    #     data = {}
    #     data = self._accumulate_amounts(data)
    #     data = self._create_non_reconciliable_move_lines(data)
    #     data = self._create_cash_statement_lines_and_cash_move_lines(data)
    #     data = self._create_invoice_receivable_lines(data)
    #     data = self._create_stock_output_lines(data)
    #     data = self._create_extra_move_lines(data)
    #     data = self._create_balancing_line(data)
    #     data = self._reconcile_account_move_lines(data)


    # def _create_account_move(self):
    #     print("_create_account_move ::")
    #     """ Create account.move and account.move.line records for this session.
    #
    #     Side-effects include:
    #         - setting self.move_id to the created account.move record
    #         - creating and validating account.bank.statement for cash payments
    #         - reconciling cash receivable lines, invoice receivable lines and stock output lines
    #     """
    #     journal = self.config_id.journal_id
    #     # Passing default_journal_id for the calculation of default currency of account move
    #     # See _get_default_currency in the account/account_move.py.
    #     account_move = self.env['account.move'].with_context(default_journal_id=journal.id).create({
    #         'journal_id': journal.id,
    #         'date': fields.Date.context_today(self),
    #         'ref': self.name,
    #     })
    #     self.write({'move_id': account_move.id})
    #
    #     ## SECTION: Accumulate the amounts for each accounting lines group
    #     # Each dict maps `key` -> `amounts`, where `key` is the group key.
    #     # E.g. `combine_receivables` is derived from pos.payment records
    #     # in the self.order_ids with group key of the `payment_method_id`
    #     # field of the pos.payment record.
    #     amounts = lambda: {'amount': 0.0, 'amount_converted': 0.0}
    #     tax_amounts = lambda: {'amount': 0.0, 'amount_converted': 0.0, 'base_amount': 0.0}
    #     split_receivables = defaultdict(amounts)
    #     split_receivables_cash = defaultdict(amounts)
    #     combine_receivables = defaultdict(amounts)
    #     combine_receivables_cash = defaultdict(amounts)
    #     invoice_receivables = defaultdict(amounts)
    #     sales = defaultdict(amounts)
    #     taxes = defaultdict(tax_amounts)
    #     stock_expense = defaultdict(amounts)
    #     stock_output = defaultdict(amounts)
    #     # Track the receivable lines of the invoiced orders' account moves for reconciliation
    #     # These receivable lines are reconciled to the corresponding invoice receivable lines
    #     # of this session's move_id.
    #     order_account_move_receivable_lines = defaultdict(lambda: self.env['account.move.line'])
    #     rounded_globally = self.company_id.tax_calculation_rounding_method == 'round_globally'
    #     print("rounded_globally",rounded_globally)
    #     for order in self.order_ids:
    #         # Combine pos receivable lines
    #         # Separate cash payments for cash reconciliation later.
    #         print("order.id ?????? ",order.id)
    #         print("order.payment_ids ????",order.payment_ids)
    #         print("order.is_invoiced ????",order.is_invoiced)
    #         for payment in order.payment_ids:
    #             amount, date = payment.amount, payment.payment_date
    #             if payment.payment_method_id.split_transactions:
    #                 if payment.payment_method_id.is_cash_count:
    #                     split_receivables_cash[payment] = self._update_amounts(split_receivables_cash[payment], {'amount': amount}, date)
    #                 else:
    #                     split_receivables[payment] = self._update_amounts(split_receivables[payment], {'amount': amount}, date)
    #             else:
    #                 key = payment.payment_method_id
    #                 if payment.payment_method_id.is_cash_count:
    #                     combine_receivables_cash[key] = self._update_amounts(combine_receivables_cash[key], {'amount': amount}, date)
    #                 else:
    #                     combine_receivables[key] = self._update_amounts(combine_receivables[key], {'amount': amount}, date)
    #
    #         if order.is_invoiced:
    #             # Combine invoice receivable lines
    #             key = order.partner_id.property_account_receivable_id.id
    #             invoice_receivables[key] = self._update_amounts(invoice_receivables[key], {'amount': order._get_amount_receivable()}, order.date_order)
    #             # side loop to gather receivable lines by account for reconciliation
    #             for move_line in order.account_move.line_ids.filtered(lambda aml: aml.account_id.internal_type == 'receivable'):
    #                 order_account_move_receivable_lines[move_line.account_id.id] |= move_line
    #         else:
    #             print("order.id",order.id)
    #             order_taxes = defaultdict(tax_amounts)
    #             for order_line in order.lines:
    #                 line = self._prepare_line(order_line)
    #                 # Combine sales/refund lines
    #                 sale_key = (
    #                     # account
    #                     line['income_account_id'],
    #                     # sign
    #                     -1 if line['amount'] < 0 else 1,
    #                     # for taxes
    #                     tuple((tax['id'], tax['account_id'], tax['tax_repartition_line_id']) for tax in line['taxes']),
    #                 )
    #                 sales[sale_key] = self._update_amounts(sales[sale_key], {'amount': line['amount']}, line['date_order'])
    #                 # Combine tax lines
    #                 for tax in line['taxes']:
    #
    #                     tax_key = (tax['account_id'], tax['tax_repartition_line_id'], tax['id'], tuple(tax['tag_ids']))
    #                     order_taxes[tax_key] = self._update_amounts(
    #                         order_taxes[tax_key],
    #                         {'amount': tax['amount'], 'base_amount': tax['base']},
    #                         tax['date_order'],
    #                         round=not rounded_globally
    #                     )
    #             print("order_taxes.items() :: ",order_taxes.items())
    #             for tax_key, amounts in order_taxes.items():
    #                 if rounded_globally:
    #                     amounts = self._round_amounts(amounts)
    #                 for amount_key, amount in amounts.items():
    #                     print("amount ::",amount)
    #                     print("taxes[tax_key][amount_key] ::",taxes[tax_key][amount_key])
    #                     taxes[tax_key][amount_key] += amount
    #
    #             if self.company_id.anglo_saxon_accounting:
    #                 # Combine stock lines
    #                 stock_moves = self.env['stock.move'].search([
    #                     ('picking_id', '=', order.picking_id.id),
    #                     ('company_id.anglo_saxon_accounting', '=', True),
    #                     ('product_id.categ_id.property_valuation', '=', 'real_time')
    #                 ])
    #                 for move in stock_moves:
    #                     exp_key = move.product_id.property_account_expense_id or move.product_id.categ_id.property_account_expense_categ_id
    #                     out_key = move.product_id.categ_id.property_stock_account_output_categ_id
    #                     amount = -sum(move.stock_valuation_layer_ids.mapped('value'))
    #                     stock_expense[exp_key] = self._update_amounts(stock_expense[exp_key], {'amount': amount}, move.picking_id.date)
    #                     stock_output[out_key] = self._update_amounts(stock_output[out_key], {'amount': amount}, move.picking_id.date)
    #
    #             # Increasing current partner's customer_rank
    #             order.partner_id._increase_rank('customer_rank')
    #
    #     ## SECTION: Create non-reconcilable move lines
    #     # Create account.move.line records for
    #     #   - sales
    #     #   - taxes
    #     #   - stock expense
    #     #   - non-cash split receivables (not for automatic reconciliation)
    #     #   - non-cash combine receivables (not for automatic reconciliation)
    #     MoveLine = self.env['account.move.line'].with_context(check_move_validity=False)
    #
    #     tax_vals = [self._get_tax_vals(key, amounts['amount'], amounts['amount_converted'], amounts['base_amount']) for key, amounts in taxes.items() if amounts['amount']]
    #     # Check if all taxes lines have account_id assigned. If not, there are repartition lines of the tax that have no account_id.
    #     tax_names_no_account = [line['name'] for line in tax_vals if line['account_id'] == False]
    #     if len(tax_names_no_account) > 0:
    #         error_message = _(
    #             'Unable to close and validate the session.\n'
    #             'Please set corresponding tax account in each repartition line of the following taxes: \n%s'
    #         ) % ', '.join(tax_names_no_account)
    #         raise UserError(error_message)
    #
    #     MoveLine.create(
    #         tax_vals
    #         + [self._get_sale_vals(key, amounts['amount'], amounts['amount_converted']) for key, amounts in sales.items()]
    #         + [self._get_stock_expense_vals(key, amounts['amount'], amounts['amount_converted']) for key, amounts in stock_expense.items()]
    #         + [self._get_split_receivable_vals(key, amounts['amount'], amounts['amount_converted']) for key, amounts in split_receivables.items()]
    #         + [self._get_combine_receivable_vals(key, amounts['amount'], amounts['amount_converted']) for key, amounts in combine_receivables.items()]
    #     )
    #
    #     ## SECTION: Create cash statement lines and cash move lines
    #     # Create the split and combine cash statement lines and account move lines.
    #     # Keep the reference by statement for reconciliation.
    #     # `split_cash_statement_lines` maps `statement` -> split cash statement lines
    #     # `combine_cash_statement_lines` maps `statement` -> combine cash statement lines
    #     # `split_cash_receivable_lines` maps `statement` -> split cash receivable lines
    #     # `combine_cash_receivable_lines` maps `statement` -> combine cash receivable lines
    #     statements_by_journal_id = {statement.journal_id.id: statement for statement in self.statement_ids}
    #     # handle split cash payments
    #     split_cash_statement_line_vals = defaultdict(list)
    #     print("split_cash_statement_line_vals " ,split_cash_statement_line_vals)
    #     split_cash_receivable_vals = defaultdict(list)
    #     partner = ''
    #     for payment, amounts in split_receivables_cash.items():
    #         print("split_receivables_cash.items()")
    #         statement = statements_by_journal_id[payment.payment_method_id.cash_journal_id.id]
    #         if payment.payment_method_id.receivable_account_id.id:
    #             is_partner = True
    #         split_cash_statement_line_vals[statement].append(self._get_statement_line_vals(is_partner,payment,statement, payment.payment_method_id.receivable_account_id, amounts['amount']))
    #         split_cash_receivable_vals[statement].append(self._get_split_receivable_vals(payment, amounts['amount'], amounts['amount_converted']))
    #         partner = payment.partner_id
    #     # handle combine cash payments
    #     combine_cash_statement_line_vals = defaultdict(list)
    #     combine_cash_receivable_vals = defaultdict(list)
    #     for payment_method, amounts in combine_receivables_cash.items():
    #         print("combine_receivables_cash.items()")
    #
    #         if not float_is_zero(amounts['amount'] , precision_rounding=self.currency_id.rounding):
    #             statement = statements_by_journal_id[payment_method.cash_journal_id.id]
    #             combine_cash_statement_line_vals[statement].append(self._get_statement_line_vals(statement, payment_method.receivable_account_id, amounts['amount']))
    #             combine_cash_receivable_vals[statement].append(self._get_combine_receivable_vals(payment_method, amounts['amount'], amounts['amount_converted']))
    #     # create the statement lines and account move lines
    #     BankStatementLine = self.env['account.bank.statement.line']
    #     split_cash_statement_lines = {}
    #     combine_cash_statement_lines = {}
    #     split_cash_receivable_lines = {}
    #     combine_cash_receivable_lines = {}
    #     print("split_cash_receivable_vals 222",split_cash_receivable_vals)
    #     print("split_cash_receivable_vals 222",len(split_cash_receivable_vals))
    #     for statement in self.statement_ids:
    #         print("statement ",statement)
    #         split_cash_statement_lines[statement] = BankStatementLine.create(split_cash_statement_line_vals[statement])
    #         combine_cash_statement_lines[statement] = BankStatementLine.create(combine_cash_statement_line_vals[statement])
    #         # line = MoveLine.create(split_cash_receivable_vals[statement])
    #         # for l in line:
    #         #     print("llllll")
    #         #     if l.account_id.id == statement.journal_id.default_debit_account_id.id:
    #         #         print("fffff")
    #         #         l.partner_id = []
    #         split_cash_receivable_lines[statement] = MoveLine.create(split_cash_receivable_vals[statement])
    #
    #         combine_cash_receivable_lines[statement] = MoveLine.create(combine_cash_receivable_vals[statement])
    #
    #     print("split_cash_receivable_lines 222",split_cash_receivable_lines)
    #     print("split_cash_receivable_lines 222",len(split_cash_receivable_lines))
    #     ## SECTION: Create invoice receivable lines for this session's move_id.
    #     # Keep reference of the invoice receivable lines because
    #     # they are reconciled with the lines in order_account_move_receivable_lines
    #     invoice_receivable_vals = defaultdict(list)
    #     invoice_receivable_lines = {}
    #     for receivable_account_id, amounts in invoice_receivables.items():
    #         invoice_receivable_vals[receivable_account_id].append(self._get_invoice_receivable_vals(receivable_account_id, amounts['amount'], amounts['amount_converted']))
    #     for receivable_account_id, vals in invoice_receivable_vals.items():
    #         invoice_receivable_lines[receivable_account_id] = MoveLine.create(vals)
    #
    #     ## SECTION: Create stock output lines
    #     # Keep reference to the stock output lines because
    #     # they are reconciled with output lines in the stock.move's account.move.line
    #     stock_output_vals = defaultdict(list)
    #     stock_output_lines = {}
    #     for output_account, amounts in stock_output.items():
    #         stock_output_vals[output_account].append(self._get_stock_output_vals(output_account, amounts['amount'], amounts['amount_converted']))
    #     for output_account, vals in stock_output_vals.items():
    #         stock_output_lines[output_account] = MoveLine.create(vals)
    #
    #     ## SECTION: Create extra move lines
    #     # Keep reference to the stock output lines because
    #     # they are reconciled with output lines in the stock.move's account.move.line
    #     MoveLine.create(self._get_extra_move_lines_vals())
    #
    #     ## SECTION: Reconcile account move lines
    #     # reconcile cash receivable lines
    #     for statement in self.statement_ids:
    #         if not self.config_id.cash_control:
    #             statement.write({'balance_end_real': statement.balance_end})
    #         statement.button_confirm_bank()
    #         all_lines = (
    #               split_cash_statement_lines[statement].mapped('journal_entry_ids').filtered(lambda aml: aml.account_id.internal_type == 'receivable')
    #             | combine_cash_statement_lines[statement].mapped('journal_entry_ids').filtered(lambda aml: aml.account_id.internal_type == 'receivable')
    #             | split_cash_receivable_lines[statement]
    #             | combine_cash_receivable_lines[statement]
    #         )
    #         accounts = all_lines.mapped('account_id')
    #         lines_by_account = [all_lines.filtered(lambda l: l.account_id == account) for account in accounts]
    #         for lines in lines_by_account:
    #             lines.reconcile()
    #
    #     # reconcile invoice receivable lines
    #     for account_id in order_account_move_receivable_lines:
    #         ( order_account_move_receivable_lines[account_id]
    #         | invoice_receivable_lines[account_id]
    #         ).reconcile()
    #
    #     # reconcile stock output lines
    #     stock_moves = self.env['stock.move'].search([('picking_id', 'in', self.order_ids.filtered(lambda order: not order.is_invoiced).mapped('picking_id').ids)])
    #     stock_account_move_lines = self.env['account.move'].search([('stock_move_id', 'in', stock_moves.ids)]).mapped('line_ids')
    #     for account_id in stock_output_lines:
    #         ( stock_output_lines[account_id]
    #         | stock_account_move_lines.filtered(lambda aml: aml.account_id == account_id)
    #         ).reconcile()

    # def _update_amounts(self, old_amounts, amounts_to_add, date, round=True, force_company_currency=False):
    #     print("old_amounts",old_amounts)
    #     print("amounts_to_add",amounts_to_add)
    #     print("date",date)
    #     print("round",round)
    #     print("force_company_currency",force_company_currency)
    #     """Responsible for adding `amounts_to_add` to `old_amounts` considering the currency of the session.
    #
    #         old_amounts {                                                       new_amounts {
    #             amount                         amounts_to_add {                     amount
    #             amount_converted        +          amount               ->          amount_converted
    #            [base_amount                       [base_amount]                    [base_amount
    #             base_amount_converted]        }                                     base_amount_converted]
    #         }                                                                   }
    #
    #     NOTE:
    #         - Notice that `amounts_to_add` does not have `amount_converted` field.
    #             This function is responsible in calculating the `amount_converted` from the
    #             `amount` of `amounts_to_add` which is used to update the values of `old_amounts`.
    #         - Values of `amount` and/or `base_amount` should always be in session's currency [1].
    #         - Value of `amount_converted` should be in company's currency
    #
    #     [1] Except when `force_company_currency` = True. It means that values in `amounts_to_add`
    #         is in company currency.
    #
    #     :params old_amounts dict:
    #         Amounts to update
    #     :params amounts_to_add dict:
    #         Amounts used to update the old_amounts
    #     :params date date:
    #         Date used for conversion
    #     :params round bool:
    #         Same as round parameter of `res.currency._convert`.
    #         Defaults to True because that is the default of `res.currency._convert`.
    #         We put it to False if we want to round globally.
    #     :params force_company_currency bool:
    #         If True, the values in amounts_to_add are in company's currency.
    #         Defaults to False because it is only used to anglo-saxon lines.
    #
    #     :return dict: new amounts combining the values of `old_amounts` and `amounts_to_add`.
    #     """
    #     # make a copy of the old amounts
    #     base_amount = 0
    #     base_amount_converted = 0
    #     new_amounts = { **old_amounts }
    #
    #     amount = amounts_to_add.get('amount')
    #     if self.is_in_company_currency or force_company_currency:
    #         amount_converted = amount
    #     else:
    #         amount_converted = self._amount_converter(amount, date, round)
    #
    #     # update amount and amount converted
    #     new_amounts['amount'] += amount
    #     print("new_amounts['amount']",new_amounts['amount'])
    #     new_amounts['amount_converted'] += amount_converted
    #     print("new_amounts['amount_converted']",new_amounts['amount_converted'])
    #     print("new_amounts ::", new_amounts)
    #
    #     # consider base_amount if present
    #     if not amounts_to_add.get('base_amount') == None:
    #         # new_amounts['base_amount_converted'] = 0
    #
    #         base_amount = amounts_to_add.get('base_amount')
    #         print("self.is_in_company_currency :: ",self.is_in_company_currency)
    #         print("self.force_company_currency :: ",force_company_currency)
    #         if self.is_in_company_currency or force_company_currency:
    #             print("enter herer ")
    #             base_amount_converted = base_amount
    #         else:
    #             print("enter herer else")
    #             print("self._amount_converter(base_amount, date, round)",self._amount_converter(base_amount, date, round))
    #
    #             base_amount_converted = self._amount_converter(base_amount, date, round)
    #
    #         # update base_amount and base_amount_converted
    #         new_amounts['base_amount_converted'] = 0.0
    #         new_amounts['base_amount'] += base_amount
    #         print("new_amounts['base_amount_converted'] :: ",new_amounts['base_amount_converted'])
    #         print("base_amount_converted :: ",base_amount_converted)
    #         new_amounts['base_amount_converted'] += base_amount_converted
    #         print("new_amounts ::",new_amounts)
    #     return new_amounts

    # def _get_split_receivable_vals(self, payment, amount, amount_converted):
    #     partial_vals = {
    #         'account_id': payment.payment_method_id.receivable_account_id.id,
    #         'move_id': self.move_id.id,
    #         # 'partner_id': self.env["res.partner"]._find_accounting_partner(payment.partner_id).id,
    #         'name': '%s - %s' % (self.name, payment.payment_method_id.name),
    #     }
    #     return self._debit_amounts(partial_vals, amount, amount_converted)
    #



    # def _get_statement_line_vals(self,is_partner,payment, statement, receivable_account, amount):
    #
    #     print('_get_statement_line_vals')
    #     print('is_partner',is_partner)
    #     if is_partner == True:
    #          id = self.env["res.partner"]._find_accounting_partner(payment.partner_id).id
    #     return {
    #         'date': fields.Date.context_today(self),
    #         'amount': amount,
    #         'name': self.name,
    #         'partner_id': id,
    #         'statement_id': statement.id,
    #         'account_id': receivable_account.id,
    #     }
    #

    def _get_statement_line_vals(self,is_partner,payment, statement, receivable_account, amount, date=False):
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
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.depends('line_ids.debit', 'line_ids.credit')
    def _cal_total_cost(self):
        for invoice in self:
            sign = -1 if invoice.type == 'out_refund' else 1
            if invoice.type in ('out_invoice', 'out_refund'):
                total_cost = 0.0
                account_type_id = self.env.ref('account.data_account_type_direct_costs')
                for line in invoice.line_ids:
                    if line.account_id.user_type_id.id == account_type_id.id:
                        total_cost += line.credit or line.debit
                invoice.total_cost = total_cost * sign
                invoice.total_profit = invoice.amount_untaxed_signed - invoice.total_cost
            else:
                invoice.total_cost = 0.0


    total_cost = fields.Float(compute='_cal_total_cost', store=True)
    total_profit = fields.Float(compute='_cal_total_cost', store=True)
    # @api.model
    # def create(self, vals_list):
    #     res = super(AccountMove, self).create(vals_list)
    #     self._cal_total_cost()
    #     return res
    #
    # def write(self, vals):
    #     res = super(AccountMove, self).write(vals)
    #     self._cal_total_cost()
    #     return res

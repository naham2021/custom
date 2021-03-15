# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _cal_total_cost(self):
        for invoice in self:
            if invoice.type in ('out_invoice', 'out_refund'):
                total_cost = 0.0
                account_type_id = self.env.ref('account.data_account_type_direct_costs')
                for line in invoice.line_ids:

                    if line.account_id.user_type_id.id == account_type_id.id:
                        total_cost += line.credit or line.debit
                invoice.total_cost = total_cost
            else:
                invoice.total_cost = 0.0

    total_cost = fields.Float( compute='_cal_total_cost')

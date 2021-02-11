# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    @api.depends('invoice_line_ids.discount', 'invoice_line_ids.price_unit', 'invoice_line_ids.quantity')
    def _cal_total_discount(self):
        for rec in self:
            total_discount = 0.0
            for line in rec.invoice_line_ids:
                total_discount += round(line.price_unit * line.quantity * line.discount / 100, 2)
            print(total_discount)
            rec.total_discount = total_discount
    total_discount = fields.Monetary(compute="_cal_total_discount")

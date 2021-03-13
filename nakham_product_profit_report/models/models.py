# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _cal_total_cost(self):
        for invoice in self:
            total_cost = 0.0
            for line in invoice.invoice_line_ids:
                if line.purchase_price:
                    total_cost += line.purchase_price
            invoice.total_cost = total_cost

    total_cost = fields.Float(digits=(16, 2), compute='_cal_total_cost')

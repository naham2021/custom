# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccounrMove(models.Model):
    _inherit = 'account.move.line'

    tax_value = fields.Float(string="Tax Value", required=False, compute="_compute_tax_value")

    def _compute_tax_value(self):
        for rec in self:
            tota_amount = 0
            for tax in rec.tax_ids:
                tota_amount += tax.amount

            if tota_amount > 0:
                rec.tax_value = rec.price_subtotal * (tota_amount / 100)
            else:
                rec.tax_value = 0

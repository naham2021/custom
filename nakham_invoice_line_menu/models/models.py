# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockLandedCost(models.Model):
    _inherit = 'stock.landed.cost'

    vendor_bill_ids = fields.Many2many(comodel_name="account.move", string="Vendor Bills",
                                       domain=[('type', '=', 'in_invoice')])
    vendor_bill_id2 = fields.Many2one(comodel_name="account.move", string="Vendor Bill 2",
                                       domain=[('type', '=', 'in_invoice')])


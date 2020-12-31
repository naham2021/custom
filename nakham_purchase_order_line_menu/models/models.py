# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    purchase_type = fields.Selection(string="Purchase Type",
                                     selection=[('local', 'Local'), ('international', 'International')],
                                     required=False)


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    remaining_qty = fields.Float(string='To be Received', compute='compute_remaining_qty', store=True)

    @api.depends('product_qty', 'qty_received')
    def compute_remaining_qty(self):
        for rec in self:
            rec.remaining_qty = rec.product_qty - rec.qty_received


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    remaining_qty = fields.Float(string='To be Delivered', compute='compute_remaining_qty', store=True)

    @api.depends('product_uom_qty', 'qty_delivered')
    def compute_remaining_qty(self):
        for rec in self:
            rec.remaining_qty = rec.product_uom_qty - rec.qty_delivered







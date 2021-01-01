# -*- coding: utf-8 -*-

from odoo import models, fields, api

class nakham_history_price_po(models.Model):
    _name = 'history.price.product'

    name = fields.Char()
    date = fields.Date(string="Date", required=False, )
    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner", required=False, )
    product_id = fields.Many2one(comodel_name="product.product", string="Product", required=False, )
    product_temp_id = fields.Many2one(comodel_name="product.template", string="Product", required=False, )
    unit_price = fields.Float(string="Unit Price",  required=False, )
    quantity = fields.Float(string="QTY",  required=False, )
    purchase_id = fields.Many2one(comodel_name="purchase.order", string="", required=False, )
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleReport(models.Model):
    _inherit = 'sale.report'

    tag_ids = fields.Many2many('product.tag', related='product_id.tag_ids')
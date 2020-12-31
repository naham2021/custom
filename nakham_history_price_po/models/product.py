# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    history_price_product_ids = fields.Many2many("history.price.product", string="History Price",compute="_compute_is_history_price_product_ids" )
    @api.depends("history_price_product_ids")
    def _compute_is_history_price_product_ids(self):
        for rec in self:
            history =  self.env['history.price.product'].search([('product_id','=',rec.id)])
            if history:
                rec.update({
                    "history_price_product_ids": [[6, 0, history.ids]]
                         })
            else:
                rec.update({
                    "history_price_product_ids": [[6, 0, []]]
                })

class ProductProduct(models.Model):
    _inherit = 'product.template'

    history_price_product_ids = fields.Many2many("history.price.product", string="History Price",
                                                 compute="_compute_is_history_price_product_ids")

    @api.depends("history_price_product_ids")
    def _compute_is_history_price_product_ids(self):
        for rec in self:
            history = self.env['history.price.product'].search([('product_temp_id', '=', rec.id)])
            if history:
                rec.update({
                    "history_price_product_ids": [[6, 0, history.ids]]
                })
            else:
                rec.update({
                    "history_price_product_ids": [[6, 0, []]]
                })
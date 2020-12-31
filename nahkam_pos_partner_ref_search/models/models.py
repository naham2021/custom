# # -*- coding: utf-8 -*-
#
# from odoo import models, fields, api
#
# class search_products_with_serial_no(models.Model):
#     _inherit = 'product.template'
#
#     @api.model
#     def get_product_id(self, product_serial):
#
#         #get lot_id from stock.production.lot  for passed product_serial
#         stock_production_lot_ids=self.env['stock.production.lot'].search([('name', '=', product_serial)]).ids
#
#         #from stock.quant "on hand quantities means available to sale" get product_ids for this lot id
#         stock_quant_recs=self.env['stock.quant'].search([('lot_id', 'in', stock_production_lot_ids)])
#
#
#         #return product_id of products have this serial number
#         products_ids=[]
#         for rec in stock_quant_recs:
#             products_ids.append(rec.product_id.id)
#         return products_ids
#

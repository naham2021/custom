# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockValuationLayer(models.Model):
    _inherit = 'stock.valuation.layer'

    categ_id = fields.Many2one('product.category', string='Product Category', related='product_id.categ_id', store=True)


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    categ_id = fields.Many2one('product.category', string='Product Category', related='product_id.categ_id', store=True)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # @api.model
    # def read_group(self, cr, uid, domain, fields, groupby, offset=0, limit=None, context=None, orderby=False,lazy=True):
    #     res = super(ProductTemplate, self).read_group(cr, uid, domain, fields, groupby, offset, limit=limit, context=context,
    #                                              orderby=orderby, lazy=lazy)
    #     if 'qty_available' in fields:
    #         for line in res:
    #             if '__domain' in line:
    #                 lines = self.search(cr, uid, line['__domain'], context=context)
    #                 qty_available = 0.0
    #                 for product in self.browse(cr, uid, lines, context=context):
    #                     qty_available += product.qty_available
    #                 line['qty_available'] = qty_available
    #     return res

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        result = super(ProductTemplate, self).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby,
                                                  lazy=lazy)
        if 'qty_available' in fields:
            for line in result:
                if '__domain' in line:
                    lines = self.search(line['__domain'])
                    qty_available_sum = 0.0
                    all_products = self.browse(lines)
                    for product in all_products.ids:
                        qty_available_sum += product.qty_available
                    line['qty_available'] = qty_available_sum
        return result






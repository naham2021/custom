from odoo import models, fields, api,_,exceptions
from odoo.addons.purchase.models.purchase import PurchaseOrder as Purchase

class purchase_order_history(models.Model):
    _inherit = 'purchase.order'

    def button_confirm(self):
        res = super(purchase_order_history, self).button_confirm()
        for line in self.order_line:
            history_price_product = self.env['history.price.product']
            history_price_product.create({
                                    'name': line.product_id.id,
                                    'date': fields.Date.today(),
                                    'partner_id': self.partner_id.id,
                                    'purchase_id': self.id,
                                    'product_id': line.product_id.id ,
                                    'product_temp_id':line.product_id.product_tmpl_id.id  ,
                                    'unit_price': line.price_unit,
                                    'quantity': line.product_qty
                                    })
        return res
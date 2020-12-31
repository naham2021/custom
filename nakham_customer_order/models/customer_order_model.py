# -*- coding: utf-8 -*-

from odoo import models, api,fields

import logging

LOGGER = logging.getLogger(__name__)


class CustomerOrderModel(models.Model):
    _name = 'customer.order'

    partner_id = fields.Many2one('res.partner', string='Customer',domain="[('customer_rank', '=', '1')]",  change_default=True, index=True, track_visibility='always', track_sequence=1, help="You can find a customer by its Name, TIN, Email or Internal Reference.")
    user_id = fields.Many2one('res.users', string='Salesperson', index=True, track_visibility='onchange', track_sequence=2, default=lambda self: self.env.user)
    location_id = fields.Many2one( related="user_id.location_id")
    order_qty = fields.Float(string='Ordered Qty' , )
    product_id = fields.Many2one('product.product', string='Product')
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure')
    date_order = fields.Date(string='Date')
    # order_line_ids = fields.Many2many(comodel_name="customer.order.line", relation="customer_order_line", column1="cu", column2="line", string="Lines", )
    order_line_ids = fields.One2many(comodel_name="customer.order.line", inverse_name="order_id", string="Lines", required=False, )

    @api.onchange('product_id')
    def onchange_method_product_id(self):
        self.product_uom = self.env['uom.uom'].search([('category_id', '=', self.product_id.uom_id.category_id.id)], limit=1).id
        return {
            'domain': {'product_uom': [('category_id', '=', self.product_id.uom_id.category_id.id)]}
        }

    def open_available_quantities(self):

        stock_quant  = self.env['stock.quant'].search([('product_id', '=', self.product_id.id),('location_id', '=', self.location_id.id)])
        LOGGER.info('herer stock :: %s',stock_quant.quantity)
        view = self.env.ref('nakham_customer_order.sh_message_wizard')
        view_id = view and view.id or False
        context =  dict(self._context or {})
        if stock_quant.quantity >= self.order_qty:
            context['message']="Variable Qty"
        else:
            context['message'] = "Not Variable Qty"
        return {
            'name':"Result",
            'type': 'ir.actions.act_window',
            'view_type':'form',
            'view_mode':'form',
            'res_model':'sh.message.wizard',
            'views':[(view.id,'form')],
            'view_id':view.id,
            'target':'new',
            'context':context
        }
        # return {
        #     'name': 'Available Quantities',
        #     'type': 'ir.actions.act_window',
        #     'view_type': 'form',
        #     'view_mode': 'tree',
        #     'res_model': 'stock.quant',
        #     'target': 'new',
        #     'domain':[("product_id", "=", self.product_id.id),("location_id.usage","=",'internal')],
        #
        # }
    def open_available_quantities_location(self):

        stock_quant  = self.env['stock.quant'].search([('product_id', '=', self.product_id.id),('location_id', '=', self.location_id.id)])
        locations  = self.env['stock.location'].search([('usage', 'in', ["internal","transit"])])
        print("locations ",locations)
        for l in locations:
            stock_quant = self.env['stock.quant'].search(
                [('product_id', '=', self.product_id.id), ('location_id', '=', l.id)])
            print("stock_quant ", stock_quant)

            total_qty = 0
            for s in stock_quant:
                print("s.value",s.value)
                print("s.inventory_quantity",s.inventory_quantity)
                print("s.quantity",s.quantity)
                print("s.location_id",s.location_id.id)
                total_qty += s.quantity

            print("total_qty",total_qty)
            if total_qty > 0:
                lines = self.env['customer.order.line'].create({
                    'location_id': s.location_id.id,
                    'order_qty': total_qty,
                    'order_id': self.id,
                })



class CustomerOrderLineModel(models.Model):
    _name = 'customer.order.line'

    location_id = fields.Many2one( 'stock.location')
    order_qty = fields.Float(string='Ordered Qty' , required=True)
    product_id = fields.Many2one('product.product', string='Product')
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure')
    order_id = fields.Many2one(comodel_name="customer.order", string="Order", required=False, )



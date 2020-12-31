# -*- coding: utf-8 -*-
from odoo import models, fields, api
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class SaleOrder(models.Model):
    _inherit = "sale.order"

    discount_type = fields.Selection(selection=[('1', 'percentage'),
                                                ('2', 'Amount'),
                                                ('3', 'Per Line')],
                                     string='Discount Type')

    discount_rate = fields.Float(string='Discount Rate',
                                 digits_compute=dp.get_precision('Account'),
                                 readonly=True,
                                 states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})

    amount_discount = fields.Float(digits_compute=dp.get_precision('Account'),
                                   string='Discount',
                                   store=True,
                                   help="The total discount.",
                                   readonly=True)

    total_before_dis = fields.Float(string='Total Before Dis', compute='compute_total_before_discount')

    def compute_discount(self, discount):
        for order in self:
            val1 = 0.0
            disc_amnt = 0.0
            for line in order.order_line:
                val1 += (line.product_uom_qty * line.price_unit)
                line.discount = round(discount, 5)
                disc_amnt += (line.product_uom_qty * line.price_unit * discount) / 100
            total = val1 + order.amount_tax - disc_amnt
            self.currency_id = order.pricelist_id.currency_id
            self.amount_discount = disc_amnt
            self.amount_total = total

    def button_dummy(self):
        self.supply_rate()
        return True

    @api.model
    def create(self, values):
        res = super(SaleOrder, self).create(values)
        res.button_dummy()
        return res

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals.update({
            'discount_type': self.discount_type,
            'discount_rate': self.discount_rate
        })
        return invoice_vals

    @api.onchange('amount_untaxed', 'amount_discount')
    def compute_total_before_discount(self):
        for rec in self:
            rec.total_before_dis = rec.amount_untaxed + rec.amount_discount

    def compute_discount_per_line(self):
        for order in self:
            val1 = val2 = 0.0
            disc_amnt = 0.0
            for line in order.order_line:
                val1 += (line.product_uom_qty * line.price_unit)
                disc_amnt += (line.product_uom_qty * line.price_unit * line.discount) / 100
            total = val1 + order.amount_tax - disc_amnt
            self.currency_id = order.pricelist_id.currency_id
            self.amount_discount = disc_amnt
            self.amount_total = total

    @api.onchange('discount_type')
    def onchange_discount_type(self):
        for order in self:
            order.discount_rate = 0

    @api.onchange('discount_type', 'discount_rate')
    def supply_rate(self):
        for order in self:
            if not order.discount_type and not order.discount_type == '3':
                order.discount_rate = 0
                self.compute_discount(0)
            else:
                if order.discount_type == '1':
                    self.compute_discount(order.discount_rate)
                elif order.discount_type == '2':
                    total = 0.0
                    for line in order.order_line:
                        total += (line.product_uom_qty * line.price_unit)
                    if total > 0:
                        discount = (order.discount_rate / total) * 100
                        self.compute_discount(discount)
                elif order.discount_type == '3':
                    order.discount_rate = 0
                    self.compute_discount_per_line()

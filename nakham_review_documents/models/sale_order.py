# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'


    review = fields.Selection(string="Review", selection=[('to_check', 'To Check'), ('checked', 'Checked'), ], required=False,default="to_check" )
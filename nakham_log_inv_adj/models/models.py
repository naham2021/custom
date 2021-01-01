# -*- coding: utf-8 -*-

from odoo import models, fields, api

class stock_inv(models.Model):
    _name = 'stock.inventory'
    _inherit = ['stock.inventory','mail.thread']

    new_note = fields.Text(string="Note", required=False, )

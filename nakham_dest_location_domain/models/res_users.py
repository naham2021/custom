# -*- coding: utf-8 -*-

from odoo import models, fields, api


class res_user_Inherit(models.Model):
    _inherit = 'res.users'


    test_location_ids=fields.Many2many('stock.location', relation="stock_location_users", column1="stock", column2="users" ,string='location',domain=[('usage', '=', 'transit')])

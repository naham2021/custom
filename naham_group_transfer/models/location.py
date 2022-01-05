# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions


class stock_location_inh(models.Model):
    _inherit = 'stock.location'

    users_ids = fields.Many2many(comodel_name="res.users", relation="users_locations", column1="user_l", column2="location_u", string="Users", )
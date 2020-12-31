# -*- coding: utf-8 -*-

from odoo import models, fields, api


class stocklocationInherit(models.Model):
    _inherit = 'stock.location'

    # user_location_ids = fields.Many2many(comodel_name="res.users", string="Users Transit", )
    user_id = fields.Many2one(comodel_name="res.users", string="", required=False, )
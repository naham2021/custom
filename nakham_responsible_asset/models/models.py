# -*- coding: utf-8 -*-

from odoo import models, fields, api

class accountAsset(models.Model):
    _inherit = 'account.asset'

    responsible_user_id = fields.Many2one(comodel_name="res.users", string="Responsible User", required=False, )


# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    user_ids = fields.Many2many(comodel_name="res.users", string="Users")

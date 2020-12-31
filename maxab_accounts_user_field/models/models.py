# -*- coding: utf-8 -*-

from odoo import models, fields, api


class maxab_accounts_rule(models.Model):
    _inherit = 'res.users'


    allowed_account_ids = fields.Many2many('account.account',string='Allowed Accounts')



# -*- coding: utf-8 -*-

from odoo import models, fields, api

class accountAccount(models.Model):
    _inherit = 'account.account'

    is_domain_partner = fields.Boolean(string="Check Account",  )


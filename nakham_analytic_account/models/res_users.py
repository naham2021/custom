# -*- coding: utf-8 -*-

from odoo import models, fields, api


class res_user_Inherit(models.Model):
    _inherit = 'res.users'


    analytic_ids=fields.Many2many('account.analytic.account', relation="account_analytic_users", column1="analytic", column2="users" ,string='Analytic Account')

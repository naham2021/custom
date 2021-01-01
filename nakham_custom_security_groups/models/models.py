# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    analytic_id = fields.Many2one('account.analytic.account', 'Analytic Account')

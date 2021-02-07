# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CrmTeamInherit(models.Model):
    _inherit = 'crm.team'

    Accountant_id = fields.Many2one('res.users', string='Accountant')




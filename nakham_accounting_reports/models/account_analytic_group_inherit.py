from odoo import models, fields, api


class AccountanalyticGroup(models.Model):
    _inherit = 'account.analytic.group'

    in_filter = fields.Boolean(string='In Filter')


from odoo import models, fields, api,tools


class naham_payment_widget(models.Model):
    _inherit = 'res.users'

    analytic_groups = fields.Many2many('account.analytic.group','analytic_rel')

    @api.onchange('analytic_groups')
    def _onchange_analytic_groups(self):
        self.clear_caches()

    @api.model
    @tools.ormcache('self._uid')
    def context_get(self):
        res = super(naham_payment_widget, self).context_get()
        new_dict = res.copy()
        new_dict['analytic_groups'] = self.env.user.analytic_groups.ids
        return new_dict




# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools

class ResUsersInherit(models.Model):
    _inherit = 'res.users'

    @api.model
    @tools.ormcache('self._uid')
    def context_get(self):
        res = super(ResUsersInherit, self).context_get()
        new_dict = res.copy()
        new_dict['allowed_account_ids'] = self.env.user.allowed_account_ids.ids
        return new_dict
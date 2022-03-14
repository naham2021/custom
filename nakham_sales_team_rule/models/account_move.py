# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountMoveLineInherit(models.Model):
    _inherit = 'account.move.line'


    current_user = fields.Many2one('res.users', 'Current User', default=lambda self: self.env.uid,compute="_get_current_user")
    # user_all = fields.Boolean(compute="_get_user_all")
    def _get_current_user(self):
        for rec in self:
            rec.current_user = self.env.uid


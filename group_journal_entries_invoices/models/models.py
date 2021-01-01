# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccounrMove(models.Model):
    _inherit = 'account.move'

    journal_visible = fields.Boolean(compute='_compute_journal_visible', default=False)

    @api.depends('type')
    def _compute_journal_visible(self):
        for rec in self:
            print('llllllllllllllllllllllll')
            print("rec.type  ",rec.type)
            print('rec.journal_visible ', rec.journal_visible)
            print('rec.journal_visible ', rec.journal_id.id)
            rec.company_id = rec.journal_id.company_id.id
            if rec.type == 'entry':
                rec.journal_visible = True
            else:
                if self.env.user.has_group('group_journal_entries_invoices.group_journal_invoices'):
                    rec.journal_visible = True
                else:
                    rec.journal_visible = False

            print('rec.journal_visible ',rec.journal_visible)
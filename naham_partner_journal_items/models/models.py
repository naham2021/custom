from odoo import models, fields, api


class naham_partner_journal_items(models.Model):
    _inherit = 'account.move.line'

    def partner_server(self):
        for r in self:
            r.partner_id = r.move_id.partner_id.id


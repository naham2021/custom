# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ResPartnerInherite(models.Model):
    _inherit = 'res.partner'



    def open_partner_ledger(self):
        return {
            'type': 'ir.actions.client',
            'name': _('Partner Ledger'),
            'tag': 'account_report',
            'options': {'partner':True,'partner_ids': [self.id]},
            'ignore_session': 'read',
            'context': "{'model':'account.partner.ledger'}"
        }

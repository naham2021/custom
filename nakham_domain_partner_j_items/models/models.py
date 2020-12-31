# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.onchange('account_id')
    def onchange_method_partner_id_account(self):
        if self.account_id:
            if self.account_id.is_domain_partner== True:
                print("enter domain")
                ids_partner = self.env['res.partner'].search(
                    ['|',('property_account_receivable_id', '=', self.account_id.id),('property_account_payable_id', '=',self.account_id.id)])
                return {'domain': {'partner_id': [('id','in',ids_partner.ids)]}}



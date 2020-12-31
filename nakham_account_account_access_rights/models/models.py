# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Partner(models.Model):
    _inherit = 'res.partner'

    property_account_payable_id = fields.Many2one('account.account', company_dependent=True, copy=True,
                                                  string="Account Payable",
                                                  domain="[('internal_type', '=', 'payable'), ('deprecated', '=', False)]",
                                                  help="This account will be used instead of the default one as the payable account for the current partner",
                                                  required=True)
    property_account_receivable_id = fields.Many2one('account.account', company_dependent=True, copy=True,
                                                     string="Account Receivable",
                                                     domain="[('internal_type', '=', 'receivable'), ('deprecated', '=', False)]",
                                                     help="This account will be used instead of the default one as the receivable account for the current partner",
                                                     required=True)


# class AccountMove(models.Model):
#     _inherit = "account.move"
#
#     journal_id = fields.Many2one('account.journal', string='Journal', required=True, readonly=True,
#                                  states={'draft': [('readonly', False)]},
#                                  domain="[('company_id', '=', company_id)]",
#                                  default=False)
#
#     currency_id = fields.Many2one('res.currency', store=True, readonly=True, tracking=True, required=True,
#                                   states={'draft': [('readonly', False)]},
#                                   string='Currency',
#                                   default=False)

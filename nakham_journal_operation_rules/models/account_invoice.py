# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import RedirectWarning, UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'


    @api.model
    def _get_default_journal(self):
        _logger.info("fied2222")
        company = self.env.company.id
        # self.company_id =company
        current_user = self.env['res.users'].browse(self.env.uid)
        _logger.info("current_user :: %s",current_user.name)
        _logger.info("current_user :: %s",current_user.sale_team_id.name)
        move_type = self._context.get('default_type', 'entry')
        journal_type = 'general'
        if move_type in self.get_sale_types(include_receipts=True):
            journal_type = 'sale'
        elif move_type in self.get_purchase_types(include_receipts=True):
            journal_type = 'purchase'
        print("journal_type :: ",journal_type)
        if journal_type == "sale":
            journal =  self.env['account.journal'].search([("user_ids", '=', current_user.id),('type','=','sale')], limit=1)
            return self.env['account.journal'].search([("id", '=', journal.id)], limit=1)
        elif journal_type == "purchase":
            journal =  self.env['account.journal'].search([("user_ids", '=', current_user.id),('type','=','purchase')], limit=1)
            print("journal 222",journal.name)
            return journal.id
        elif journal_type == "sale":
            journal = self.env['account.journal'].search([("user_ids", '=', current_user.id),('type','=','sale')], limit=1)
            return self.env['account.journal'].search([("id", '=', journal.id)], limit=1)
        elif journal_type == "purchase":
            journal =  self.env['account.journal'].search([("user_ids", '=', current_user.id)], limit=1)
            return self.env['account.journal'].search([("id", '=', journal.id),('type','=','purchase')], limit=1)
        elif journal_type == "general":
            journal =  self.env['account.journal'].search([("user_ids", '=', current_user.id)], limit=1)
            return self.env['account.journal'].search([("id", '=', journal.id)], limit=1)
    @api.model
    def _get_default_currency_new(self):
        journal = self._default_journal()
        print('journal ::::',journal)
        j = self.env['account.journal'].search([("id", '=', journal.id)], limit=1)
        print('j ',j.name)
        return j.currency_id or j.company_id.currency_id


    currency_id = fields.Many2one('res.currency', store=True, readonly=True, tracking=True, required=True,
        states={'draft': [('readonly', False)]},
        string='Currency',
        default=_get_default_currency_new)

    @api.model
    def _default_journal(self):
        # return False
        _logger.info("fied")
        company = self.env.company.id
        # self.company_id =company
        current_user = self.env['res.users'].browse(self.env.uid)
        _logger.info("current_user :: %s",current_user.name)
        _logger.info("current_user :: %s",current_user.sale_team_id.name)
        type=self.env.context.get('default_type')
        print("type :: ",type)
        if type == "out_invoice":
            journal =  self.env['account.journal'].search([("user_ids", '=', current_user.id),('type','=','sale')], limit=1)
            return self.env['account.journal'].search([("id", '=', journal.id)], limit=1)
        elif type == "in_invoice":
            journal =  self.env['account.journal'].search([("user_ids", '=', current_user.id),('type','=','purchase')], limit=1)
            print("journal ",journal.name)
            return self.env['account.journal'].search([("id", '=', journal.id)], limit=1)
        elif type == "out_refund":
            journal = self.env['account.journal'].search([("user_ids", '=', current_user.id),('type','=','sale')], limit=1)
            return self.env['account.journal'].search([("id", '=', journal.id)], limit=1)
        elif type == "in_refund":
            journal =  self.env['account.journal'].search([("user_ids", '=', current_user.id)], limit=1)
            return self.env['account.journal'].search([("id", '=', journal.id),('type','=','purchase')], limit=1)
        else:
            journal = self.env['account.journal'].search([("user_ids", '=', current_user.id)], limit=1)
            return self.env['account.journal'].search([("id", '=', journal.id)], limit=1)

    journal_id = fields.Many2one('account.journal', string='Journal',
        required=True, readonly=True, states={'draft': [('readonly', False)]},
        default=_default_journal)

    @api.onchange('journal_id')
    def _onchange_journal_id_sale(self):
        current_user = self.env['res.users'].browse(self.env.uid)
        journal =  self.env['account.journal'].search([("user_ids", '=', current_user.id)], limit=1)
        if self.type == "out_invoice":
            journal =  self.env['account.journal'].search([("user_ids", '=', current_user.id),('type','=','sale')])
            return {
                'domain': { 'journal_id': [('id', '=', journal.ids   )]}
            }
        elif self.type == "in_invoice":
            journal =  self.env['account.journal'].search([("user_ids", '=', current_user.id),('type','=','purchase')])
            return {
                'domain': {'journal_id': [('id', '=', journal.ids)]}
            }
        elif self.type == "out_refund":
            journal =  self.env['account.journal'].search([("user_ids", '=', current_user.id),('type','=','sale')])
            return {
                'domain': { 'journal_id': [('id', '=', journal.ids   )]}
            }
        elif self.type == "in_refund":
            journal =  self.env['account.journal'].search([("user_ids", '=', current_user.id),('type','=','purchase')])
            return {
                'domain': {'journal_id': [('id', '=', journal.ids)]}
            }
        else:
            journal =  self.env['account.journal'].search([(1, '=',1)])
            return {
                'domain': {'journal_id': [('id', 'in', journal.ids)]}
            }




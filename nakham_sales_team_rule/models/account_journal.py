# -*- coding: utf-8 -*-

import json
from datetime import datetime, timedelta

from babel.dates import format_datetime, format_date
from odoo import models, api, _, fields
from odoo.osv import expression
from odoo.release import version
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF, safe_eval
from odoo.tools.misc import formatLang, format_date as odoo_format_date, get_lang
import random

import ast

class AccountJournalInherit(models.Model):
    _inherit = 'account.journal'

    def open_action_member(self):
        """return action based on type for related journals"""
        action_name = self._context.get('action_name')

        # Find action based on journal.
        if not action_name:
            if self.type == 'bank':
                action_name = 'account.action_bank_statement_tree'
            elif self.type == 'cash':
                action_name = 'account.action_view_bank_statement_tree'
            elif self.type == 'sale':
                action_name = 'nakham_sales_team_rule.action_move_out_invoice_type_member'
            elif self.type == 'purchase':
                action_name = 'account.action_move_in_invoice_type'
            else:
                action_name = 'account.action_move_journal_line'

        # Set 'account.' prefix if missing.
        # if '.' not in action_name:
        #     action_name = 'account.%s' % action_name

        action = self.env.ref(action_name).read()[0]
        context = self._context.copy()
        if 'context' in action and type(action['context']) == str:
            context.update(ast.literal_eval(action['context']))
        else:
            context.update(action.get('context', {}))
        action['context'] = context
        action['context'].update({
            'default_journal_id': self.id,
            'search_default_journal_id': self.id,
        })

        domain_type_field = action['res_model'] == 'account.move.line' and 'move_id.type' or 'type' # The model can be either account.move or account.move.line

        # Override the domain only if the action was not explicitly specified in order to keep the
        # original action domain.
        if not self._context.get('action_name'):
            if self.type == 'sale':
                action['domain'] = [(domain_type_field, 'in', ('out_invoice', 'out_refund', 'out_receipt')),('invoice_user_id','=',self.env.uid)]
            elif self.type == 'purchase':
                action['domain'] = [(domain_type_field, 'in', ('in_invoice', 'in_refund', 'in_receipt')),('invoice_user_id','=',self.env.uid)]

        return action
    def open_action_manager(self):
        """return action based on type for related journals"""
        action_name = self._context.get('action_name')

        # Find action based on journal.
        if not action_name:
            if self.type == 'bank':
                action_name = 'account.action_bank_statement_tree'
            elif self.type == 'cash':
                action_name = 'account.action_view_bank_statement_tree'
            elif self.type == 'sale':
                action_name = 'nakham_sales_team_rule.action_move_out_invoice_type_manager'
            elif self.type == 'purchase':
                action_name = 'account.action_move_in_invoice_type'
            else:
                action_name = 'account.action_move_journal_line'

        # Set 'account.' prefix if missing.
        # if '.' not in action_name:
        #     action_name = 'account.%s' % action_name

        action = self.env.ref(action_name).read()[0]
        context = self._context.copy()
        if 'context' in action and type(action['context']) == str:
            context.update(ast.literal_eval(action['context']))
        else:
            context.update(action.get('context', {}))
        action['context'] = context
        action['context'].update({
            'default_journal_id': self.id,
            'search_default_journal_id': self.id,
        })

        domain_type_field = action['res_model'] == 'account.move.line' and 'move_id.type' or 'type' # The model can be either account.move or account.move.line

        # Override the domain only if the action was not explicitly specified in order to keep the
        # original action domain.
        if not self._context.get('action_name'):
            if self.type == 'sale':
                action['domain'] = [(domain_type_field, 'in', ('out_invoice', 'out_refund', 'out_receipt')),('team_id.user_id','=',self.env.uid)]
            elif self.type == 'purchase':
                action['domain'] = [(domain_type_field, 'in', ('in_invoice', 'in_refund', 'in_receipt')),('team_id.user_id','=',self.env.uid)]

        return action
    def open_action_accountant(self):
        """return action based on type for related journals"""
        action_name = self._context.get('action_name')

        # Find action based on journal.
        if not action_name:
            if self.type == 'bank':
                action_name = 'account.action_bank_statement_tree'
            elif self.type == 'cash':
                action_name = 'account.action_view_bank_statement_tree'
            elif self.type == 'sale':
                action_name = 'nakham_sales_team_rule.action_move_out_invoice_type_accountant'
            elif self.type == 'purchase':
                action_name = 'account.action_move_in_invoice_type'
            else:
                action_name = 'account.action_move_journal_line'

        # Set 'account.' prefix if missing.
        # if '.' not in action_name:
        #     action_name = 'account.%s' % action_name

        action = self.env.ref(action_name).read()[0]
        context = self._context.copy()
        if 'context' in action and type(action['context']) == str:
            context.update(ast.literal_eval(action['context']))
        else:
            context.update(action.get('context', {}))
        action['context'] = context
        action['context'].update({
            'default_journal_id': self.id,
            'search_default_journal_id': self.id,
        })

        domain_type_field = action['res_model'] == 'account.move.line' and 'move_id.type' or 'type' # The model can be either account.move or account.move.line

        # Override the domain only if the action was not explicitly specified in order to keep the
        # original action domain.
        if not self._context.get('action_name'):
            if self.type == 'sale':
                action['domain'] = [(domain_type_field, 'in', ('out_invoice', 'out_refund', 'out_receipt')),('team_id.Accountant_id','=',self.env.uid)]
            elif self.type == 'purchase':
                action['domain'] = [(domain_type_field, 'in', ('in_invoice', 'in_refund', 'in_receipt')),('team_id.Accountant_id','=',self.env.uid)]

        return action

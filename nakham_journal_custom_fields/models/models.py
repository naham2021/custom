# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    payment_id = fields.Many2one('account.payment', string="Originator Payment",
                                 help="Payment that created this entry")
    picking_id = fields.Many2one('stock.picking', related='stock_move_id.picking_id')
    account_bank_statement_id = fields.Many2one('account.bank.statement')


class AccountPayment(models.Model):
    _inherit = "account.payment"

    def _prepare_payment_moves(self):
        all_move_vals = super(AccountPayment, self)._prepare_payment_moves()
        for dic in all_move_vals:
            dic.update({
                'payment_id': self.id,
            })
        return all_move_vals


class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"

    def _prepare_reconciliation_move(self, move_ref):
        all_move_vals = super(AccountBankStatementLine, self)._prepare_reconciliation_move(move_ref)
        all_move_vals.update({
            'account_bank_statement_id': self.statement_id.id,
        })
        return all_move_vals


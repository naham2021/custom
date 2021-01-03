# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    def unlink(self):
        for move in self:
            if move.name != '/' and not self._context.get('force_delete'):
                print("pass")
                # raise UserError(_("You cannot delete an entry which has been posted once."))
            move.line_ids.unlink()
        return super(AccountMove, self).unlink()


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def unlink(self):
        moves = self.mapped('move_id')

        # Prevent deleting lines on posted entries
        if any(m.state == 'posted' for m in moves):
            print("pass")
            # raise UserError(_('You cannot delete an item linked to a posted entry.'))

        # Check the lines are not reconciled (partially or not).
        self._check_reconciliation()

        # Check the lock date.
        moves._check_fiscalyear_lock_date()

        # Check the tax lock date.
        self._check_tax_lock_date()

        res = super(AccountMoveLine, self).unlink()

        # Check total_debit == total_credit in the related moves.
        if self._context.get('check_move_validity', True):
            moves._check_balanced()

        return res



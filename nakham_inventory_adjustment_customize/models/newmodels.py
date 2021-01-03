# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime


class StockInventory(models.Model):
    _inherit = 'stock.inventory'

    name = fields.Char(
        'Inventory Reference', default="New",copy=False,
        readonly=True, required=True)
    adjust_journal_id = fields.Many2one('account.journal', string='Journal', domain="[('type', '=', 'general')]")

    @api.model
    def create(self, vals):
        print('mmmm')
        if vals.get('name', _('New')) == _('New'):
            print('jjjjjjj')
            year = datetime.strptime(str(datetime.now().date()), '%Y-%m-%d').strftime('%Y')
            # datetime.now().date()
            vals['name'] = self.env['ir.sequence'].next_by_code('stock.inventory') or _('New')
            vals['name'] += '/' + year
        result = super(StockInventory, self).create(vals)
        return result

    def copy_data(self, default=None):
        res = super(StockInventory, self).copy_data(default)
        print('resssssssssssssssssssssss >> >> ',res)
        for rec in res:
            rec['name'] = _('New')
        return res


class AccountMove(models.Model):
    _inherit = 'account.move'

    inventory_id = fields.Many2one(comodel_name="stock.inventory")


class StockMove(models.Model):
    _inherit = 'stock.move'

    adjust_journal_id = fields.Many2one('account.journal', string='Journal')

    def _create_account_move_line(self, credit_account_id, debit_account_id, journal_id, qty, description, svl_id,
                                  cost):
        print("_create_account_move_line :: ")
        self.ensure_one()

        AccountMove = self.env['account.move'].with_context(default_journal_id=journal_id)

        move_lines = self._prepare_account_move_line(qty, cost, credit_account_id, debit_account_id, description)
        print("scrapped :: --> ", self.scrapped)
        if self.scrapped == True:
            print("self.scrapped :: --> ", self.scrapped)

            print("move_lines :: --> ", move_lines)
            for line in move_lines:
                print("herere")
                print("line 000 ",line)
                account = self.env['account.account'].search([('id', '=', line[2]['account_id'])], limit=1)
                product = self.env['product.product'].search([('id', '=', line[2]['product_id'])], limit=1)
                user = self.env['res.users'].search([('id', '=', self.env.uid)], limit=1)
                analytic = self.env['account.analytic.account'].search([('id', '=', user.analytic_ids.ids)], limit=1)
                print("account :: --> ", account)
                print("product :: --> ", product)
                print("user :: --> ", user)
                print("analytic :: --> ", analytic)

                if account.id != product.categ_id.property_stock_valuation_account_id.id:
                    line[2]['analytic_account_id']= analytic.id

        if self.inventory_id.id:
            print("self.adjust_journal_id :: --> ", self.adjust_journal_id)

            print("move_lines :: --> ", move_lines)
            for line in move_lines:
                print("herere")
                print("line 000 ",line)
                account = self.env['account.account'].search([('id', '=', line[2]['account_id'])], limit=1)
                product = self.env['product.product'].search([('id', '=', line[2]['product_id'])], limit=1)
                user = self.env['res.users'].search([('id', '=', self.env.uid)], limit=1)
                analytic = self.env['account.analytic.account'].search([('id', '=', user.analytic_ids.ids)], limit=1)
                print("account :: --> ", account)
                print("product :: --> ", product)
                print("user :: --> ", user)
                print("analytic :: --> ", analytic)

                if account.id != product.categ_id.property_stock_valuation_account_id.id:
                    line[2]['analytic_account_id']= analytic.id



        if move_lines:
            if self.adjust_journal_id:
                date = self._context.get('force_period_date', fields.Date.context_today(self))
                new_account_move = AccountMove.sudo().create({
                    'journal_id': self.adjust_journal_id.id,
                    'inventory_id': self.inventory_id.id,
                    'line_ids': move_lines,
                    'date': date,
                    'ref': description,
                    'stock_move_id': self.id,
                    'stock_valuation_layer_ids': [(6, None, [svl_id])],
                    'type': 'entry',
                })
            else:
                date = self._context.get('force_period_date', fields.Date.context_today(self))
                new_account_move = AccountMove.sudo().create({
                    'journal_id': journal_id,
                    'inventory_id': self.inventory_id.id,
                    'line_ids': move_lines,
                    'date': date,
                    'ref': description,
                    'stock_move_id': self.id,
                    'stock_valuation_layer_ids': [(6, None, [svl_id])],
                    'type': 'entry',
                })
            new_account_move.post()


class InventoryLine(models.Model):
    _inherit = "stock.inventory.line"

    adjust_journal_id = fields.Many2one('account.journal', related='inventory_id.adjust_journal_id')

    def _get_move_values(self, qty, location_id, location_dest_id, out):
        self.ensure_one()
        return {
            'name': _('INV:') + (self.inventory_id.name or ''),
            'product_id': self.product_id.id,
            'product_uom': self.product_uom_id.id,
            'product_uom_qty': qty,
            'date': self.inventory_id.date,
            'company_id': self.inventory_id.company_id.id,
            'inventory_id': self.inventory_id.id,
            'adjust_journal_id': self.adjust_journal_id.id,
            'state': 'confirmed',
            'restrict_partner_id': self.partner_id.id,
            'location_id': location_id,
            'location_dest_id': location_dest_id,
            'move_line_ids': [(0, 0, {
                'product_id': self.product_id.id,
                'lot_id': self.prod_lot_id.id,
                'product_uom_qty': 0,  # bypass reservation here
                'product_uom_id': self.product_uom_id.id,
                'qty_done': qty,
                'package_id': out and self.package_id.id or False,
                'result_package_id': (not out) and self.package_id.id or False,
                'location_id': location_id,
                'location_dest_id': location_dest_id,
                'owner_id': self.partner_id.id,
            })]
        }

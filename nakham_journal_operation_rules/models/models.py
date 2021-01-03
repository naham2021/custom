# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountJournalInherit(models.Model):
    _inherit='account.journal'

    user_ids=fields.Many2many('res.users',string='Users')


class OperationTypeInherit(models.Model):
    _inherit = 'stock.picking.type'

    user_ids = fields.Many2many('res.users', string='Users')

class StockWarehouseInherit(models.Model):
    _inherit = 'stock.warehouse'

    user_ids = fields.Many2many('res.users', string='Users')
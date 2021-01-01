# -*- coding: utf-8 -*-

from odoo import models, fields, api

class pos_payment(models.Model):
    _inherit = 'pos.payment'

    account_move_id = fields.Many2one(related="pos_order_id.account_move",comodel_name="account.move", string="Invoice", required=False, )
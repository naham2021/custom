# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'


    team_id = fields.Many2one('crm.team',related="order_id.team_id", string='Sales Team',store=True)
    user_id = fields.Many2one(related='order_id.user_id', string='User')

# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class nakham_warehouse_analytic_account(models.Model):
#     _name = 'nakham_warehouse_analytic_account.nakham_warehouse_analytic_account'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
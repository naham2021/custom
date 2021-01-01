# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class nakham_journals_invoices(models.Model):
#     _name = 'nakham_journals_invoices.nakham_journals_invoices'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
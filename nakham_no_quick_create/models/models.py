# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class nakham_no_quick_create(models.Model):
#     _name = 'nakham_no_quick_create.nakham_no_quick_create'
#     _description = 'nakham_no_quick_create.nakham_no_quick_create'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

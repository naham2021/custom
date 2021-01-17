# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class nakham_sales_record_rules(models.Model):
#     _name = 'nakham_sales_record_rules.nakham_sales_record_rules'
#     _description = 'nakham_sales_record_rules.nakham_sales_record_rules'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

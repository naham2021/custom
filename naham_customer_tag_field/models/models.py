# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class naham_customer_tag_field(models.Model):
#     _name = 'naham_customer_tag_field.naham_customer_tag_field'
#     _description = 'naham_customer_tag_field.naham_customer_tag_field'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

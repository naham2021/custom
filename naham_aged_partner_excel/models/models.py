# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class naham_aged_partner_excel(models.Model):
#     _name = 'naham_aged_partner_excel.naham_aged_partner_excel'
#     _description = 'naham_aged_partner_excel.naham_aged_partner_excel'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

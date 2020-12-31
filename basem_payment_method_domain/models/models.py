# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class basem_domain_product_by_vendor(models.Model):
#     _name = 'basem_domain_product_by_vendor.basem_domain_product_by_vendor'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
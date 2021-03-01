# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class naham_invoice_print_security(models.Model):
#     _name = 'naham_invoice_print_security.naham_invoice_print_security'
#     _description = 'naham_invoice_print_security.naham_invoice_print_security'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

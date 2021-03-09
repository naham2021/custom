# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class naham_inventory_cancel_button_security(models.Model):
#     _name = 'naham_inventory_cancel_button_security.naham_inventory_cancel_button_security'
#     _description = 'naham_inventory_cancel_button_security.naham_inventory_cancel_button_security'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

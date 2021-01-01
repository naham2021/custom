# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class nakham_group_to_draft_invoice(models.Model):
#     _name = 'nakham_group_to_draft_invoice.nakham_group_to_draft_invoice'
#     _description = 'nakham_group_to_draft_invoice.nakham_group_to_draft_invoice'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

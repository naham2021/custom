# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class nakham_group_to_draft_payment(models.Model):
#     _name = 'nakham_group_to_draft_payment.nakham_group_to_draft_payment'
#     _description = 'nakham_group_to_draft_payment.nakham_group_to_draft_payment'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

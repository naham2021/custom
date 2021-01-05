# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class nakham_edit_partner_ladger(models.Model):
#     _name = 'nakham_edit_partner_ladger.nakham_edit_partner_ladger'
#     _description = 'nakham_edit_partner_ladger.nakham_edit_partner_ladger'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

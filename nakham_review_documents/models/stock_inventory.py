# -*- coding: utf-8 -*-

from odoo import models, fields, api


class stockinventoryInherit(models.Model):
    _inherit = 'stock.inventory'

    review = fields.Selection(string="Review", selection=[('to_check', 'To Check'), ('checked', 'Checked'), ], required=False,default="to_check" )
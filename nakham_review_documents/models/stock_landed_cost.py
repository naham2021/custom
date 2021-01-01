# -*- coding: utf-8 -*-

from odoo import models, fields, api


class stockstocklandedcostInherit(models.Model):
    _inherit = 'stock.landed.cost'

    review = fields.Selection(string="Review", selection=[('to_check', 'To Check'), ('checked', 'Checked'), ], required=False,default="to_check" )
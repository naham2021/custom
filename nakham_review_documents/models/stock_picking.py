# -*- coding: utf-8 -*-

from odoo import models, fields, api


class stockPickingInherit(models.Model):
    _inherit = 'stock.picking'

    review = fields.Selection(string="Review", selection=[('to_check', 'To Check'), ('checked', 'Checked'), ], required=False,default="to_check" )
    origin = fields.Char(
        'Source Document', index=True,
        states={'done': [('readonly', False)], 'cancel': [('readonly', False)]},
        help="Reference of the document")
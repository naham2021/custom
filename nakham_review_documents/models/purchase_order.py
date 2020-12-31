# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    review = fields.Selection(string="Review", selection=[('to_check', 'To Check'), ('checked', 'Checked'), ],
                          required=False, default="to_check")






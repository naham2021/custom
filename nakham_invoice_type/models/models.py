# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    invoice_type = fields.Selection(string="Invoice Type",
                                    selection=[('credit', 'Credit'),
                                               ('cash', 'Cash'), ],
                                    required=True,
                                    default='cash')


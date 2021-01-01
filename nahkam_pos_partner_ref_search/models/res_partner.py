# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    barcode = fields.Char(related='ref',
                          store=True,
                          help="Use a barcode to identify this contact from the Point of Sale.",
                          copy=False,
                          readonly=False)

    def set_barcode(self):
        for rec in self.env['res.partner'].search([]):
            rec.barcode = rec.ref

    salesperson_name = fields.Char(related='user_id.name', store=True, copy=False)
    area_name = fields.Char(related='area_id.name', readonly=True)




# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_customer = fields.Boolean(string="Customer",compute="_compute_is_customer"  )

    @api.depends("customer_rank")
    def _compute_is_customer(self):

        for rec in self:
            print("rec.customer_rank",rec.customer_rank)
            if rec.customer_rank >= 0:
                print("if")
                rec.is_customer = True
            else:
                print("else")
                rec.is_customer = False
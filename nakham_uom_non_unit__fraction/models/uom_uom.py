# -*- coding: utf-8 -*-

from odoo import models, fields, api

class UomUomInherit(models.Model):
    _inherit = 'uom.uom'

    is_non_fraction = fields.Boolean('Non-Unit Fraction')

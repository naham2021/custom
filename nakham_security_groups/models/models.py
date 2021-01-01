# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import ValidationError


class res_users_inherit(models.Model):
    _inherit = 'res.users'

    area_ids = fields.Many2many('partner.area', string='Area')
class product_template(models.Model):
    _inherit = 'product.template'

    @api.constrains('default_code')
    def unique_default_code(self):
        if self.default_code and self.search([('default_code', '=', self.default_code),
                                                     ('id', '!=', self.id)]):
            raise ValidationError(_('Internal Reference already exists!'))
class product_product(models.Model):
    _inherit = 'product.product'

    @api.constrains('default_code')
    def unique_default_code_product(self):
        if self.default_code and self.search([('default_code', '=', self.default_code),
                                                     ('id', '!=', self.id)]):
            raise ValidationError(_('Internal Reference already exists!'))


class res_partner_inherit(models.Model):
    _inherit='res.partner'

    ref = fields.Char(string='Reference', index=True,copy=False)


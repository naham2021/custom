# -*- coding: utf-8 -*-

from collections import Counter
from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare



class stock_move_line(models.Model):
    _inherit = 'stock.move.line'

    @api.onchange('qty_done')
    def onchange_method_qty_done(self):
        if self.product_id.id != False:
            if self.product_uom_id.id == False:
                raise ValidationError(_("Sorry .. you must Selected Product And UOM !!"))

            if self.product_uom_id.is_non_fraction == True:
                if self.qty_done%1 != 0:
                    raise ValidationError(_("Sorry .. you must Enter Integer Number !!"))



class stock_move_line(models.Model):
    _inherit = 'stock.move'

    @api.onchange('quantity_done')
    def onchange_method_quantity_done(self):
        if self.product_id.id != False:
            if self.product_uom.id == False:
                raise ValidationError(_("Sorry .. you must Selected Product And UOM !!"))

            if self.product_uom.is_non_fraction == True:
                if self.qty_done%1 != 0:
                    raise ValidationError(_("Sorry .. you must Enter Integer Number !!"))


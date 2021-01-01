# -*- coding: utf-8 -*-
from odoo import models, fields, api,_
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class PurchaseOrderInherite(models.Model):
    _inherit = "purchase.order"

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            seq_date = None
            if 'date_order' in vals:
                seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(vals['date_order']))

            deliver_to	 = self.env['stock.picking.type'].search([('id', '=', vals['picking_type_id'])], limit=1)

            v = self.env['ir.sequence'].next_by_code('purchase.order', sequence_date=seq_date) or '/'
            vals['name'] = str(deliver_to.warehouse_id.code) + '/' + v
        return super(PurchaseOrderInherite, self).create(vals)

# -*- coding: utf-8 -*-
from odoo import models, fields, api,_
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class SaleOrderInherite(models.Model):
    _inherit = "sale.order"

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            seq_date = None
            if 'date_order' in vals:
                seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(vals['date_order']))
            if 'company_id' in vals:
                 v = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code(
                    'sale.order', sequence_date=seq_date) or _('New')
                 warehouse = self.env['stock.warehouse'].search([('id', '=', vals['warehouse_id'])], limit=1)
                 vals['name'] = str(warehouse.code)+ '/' + v
            else:
                warehouse = self.env['stock.warehouse'].search([('id', '=', vals['warehouse_id'])], limit=1)
                v = vals['warehouse_id'] + self.env['ir.sequence'].next_by_code('sale.order', sequence_date=seq_date) or _('New')
                vals['name'] = str(warehouse.code) + '/' + v

        result = super(SaleOrderInherite, self).create(vals)
        return result
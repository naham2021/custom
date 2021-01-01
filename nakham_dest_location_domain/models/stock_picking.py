# -*- coding: utf-8 -*-

from odoo import models, fields, api


class stockPickingInherit(models.Model):
    _inherit = 'stock.picking'

    # user_location_ids = fields.Many2many(comodel_name="res.users", string="Users Transit", )
    @api.onchange('location_dest_id')
    def onchange_method_location_dest_id(self):
        if self.picking_type_id.code == 'incoming':
            types = self.env['stock.picking.type'].search(
                [('user_ids', '=', self.env.user.id )])
            # print("types : : " ,types)
            ids = []
            for t in types:
                # print('t.warehouse_id',t.warehouse_id)
                # print('t.t.warehouse_id.in_type_id.id',t.warehouse_id.lot_stock_id.id)
                ids.append(t.warehouse_id.lot_stock_id.id)

            # print('ids -- > ',ids)
            return {
                'domain': {'location_dest_id': [('id', 'in', ids)]}
            }
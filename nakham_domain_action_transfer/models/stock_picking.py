# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'

    # new_field_ids = fields.Many2many(comodel_name="", relation="", column1="", column2="", string="", )
    user_warehouse_ids = fields.Many2many('res.users',string='User Warehouse',relation="rel_user_opertion_ware", column1="rel", column2="o_p",store=True)
    is_user = fields.Boolean(string="Is User",compute='compute_user_warehouse_ids'  )
    def do_user_w(self):
        for rec in self:
            rec.is_user = True
            print("rec.picking_type_id.user_ids.ids",rec.picking_type_id.user_ids.ids)
            if rec.picking_type_id.user_ids.ids != []:
                rec.user_warehouse_ids = [(6, 0, rec.picking_type_id.user_ids.ids)]
            else:
                rec.user_warehouse_ids = [(6, 0, [])]

    @api.depends("picking_type_id")
    def compute_user_warehouse_ids(self):
        for rec in self:
            rec.sudo().do_user_w()



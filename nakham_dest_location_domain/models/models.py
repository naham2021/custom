# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'

    location_dest_id = fields.Many2one(
        'stock.location', "Destination Location",
        default=False,
        readonly=True, required=True,
        states={'draft': [('readonly', False)]})

    @api.onchange('picking_type_id', 'partner_id')
    def onchange_picking_type(self):
        if self.picking_type_id:
            if self.picking_type_id.default_location_src_id:
                location_id = self.picking_type_id.default_location_src_id.id
            elif self.partner_id:
                location_id = self.partner_id.property_stock_supplier.id
            else:
                customerloc, location_id = self.env['stock.warehouse']._get_partner_locations()

            if self.picking_type_id.default_location_dest_id:
                location_dest_id = False
            elif self.partner_id:
                location_dest_id = self.partner_id.property_stock_customer.id
            else:
                location_dest_id, supplierloc = self.env['stock.warehouse']._get_partner_locations()

            if self.state == 'draft':
                self.location_id = location_id
                self.location_dest_id = location_dest_id
        # TDE CLEANME move into onchange_partner_id
        if self.partner_id and self.partner_id.picking_warn:
            if self.partner_id.picking_warn == 'no-message' and self.partner_id.parent_id:
                partner = self.partner_id.parent_id
            elif self.partner_id.picking_warn not in ('no-message', 'block') and self.partner_id.parent_id.picking_warn == 'block':
                partner = self.partner_id.parent_id
            else:
                partner = self.partner_id
            if partner.picking_warn != 'no-message':
                if partner.picking_warn == 'block':
                    self.partner_id = False
                return {'warning': {
                    'title': ("Warning for %s") % partner.name,
                    'message': partner.picking_warn_msg
                }}

    @api.onchange('location_dest_id')
    def onchange_location_dest(self):
        for rec in self:
            if rec.location_dest_id:
                for line in rec.move_line_ids_without_package:
                    line.location_dest_id = rec.location_dest_id.id

            print("location :: %s", self.env.user.test_location_ids.ids)
        return {
            'domain': {'location_dest_id': [('id', 'in', self.env.user.test_location_ids.ids)]}
        }
#     # @api.multi
#     # def get_default_dest_location(self):
#     #     for rec in self:
#     #         rec.location_dest_id = [(5, 0, 0)]
#
#
#
#     # _defaults = {
#     #     'location_dest_id': False,
#     # }
#
#
#      # @api.model
# #     # def create(self):
# #     #     res


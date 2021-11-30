from odoo import api, models, fields
from odoo.osv import osv
import odoo.addons.decimal_precision as dp


class AccountInvoice(models.Model):
    _inherit = "account.move"

    # def find_warehouse(self,location):
    #     print('location ',location)
    #     location_c = self.env['stock.location'].search([('id', '=',
    #                                              location)], limit=1)
    #     if location_c.usage == 'view':
    #         print("here view")
    #         w = self.env['stock.warehouse'].search([('view_location_id', '=',
    #                                                      location_c.id)],limit=1)
    #         print("wwwww ",w.id)
    #         id_k = w.id
    #         print("wwwww ",id_k)
    #         return id_k
    #     else:
    #         self.find_warehouse(location_c.location_id.id)
    warehouse_char = fields.Char(string="Warehouse", required=False,compute="_compute_warehouse" )
    analytic_account_id = fields.Many2one(comodel_name="account.analytic.account", string="Analytic Account", required=False,compute="_compute_warehouse" )
    @api.depends('ref')
    def _compute_warehouse(self):
        for rec in self:
            # pos_order = self.env['pos.order'].search([('name', '=',
            #                                            rec.ref)])



            sale_order = self.env['sale.order'].search([('name', '=',
                                                       rec.ref)])
            # if pos_order:
            #     # print('self.find_warehouse(pos_order.location_id.id)',rec.find_warehouse(pos_order.location_id.id))
            #     # w = rec.find_warehouse(pos_order.location_id.id)
            #     # w_l = self.env['stock.warehouse'].search([('id', '=',
            #     #                                          w)], limit=1)
            #     # print("w  -->:: ",w_l)
            #     # rec.warehouse_char = w_l.code
            #     rec.warehouse_char = pos_order.picking_id.picking_type_id.warehouse_id.code
            #     rec.analytic_account_id = pos_order.picking_id.picking_type_id.warehouse_id.analytic_account_id.id
            if sale_order:
                rec.warehouse_char = sale_order.warehouse_id.code
                rec.analytic_account_id = sale_order.warehouse_id.analytic_account_id.id
            else:
                rec.warehouse_char = ''
                rec.analytic_account_id = []




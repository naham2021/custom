# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountPaymentInherit(models.Model):
    _inherit = 'account.payment'

    payment_user_id = fields.Many2one(
        'res.users', string='Responsible',
        required=True,
        readonly=False,
        default=lambda self: self.env.uid,)
    team_id = fields.Many2one('crm.team', string='Store', oldname='section_id',
                              default=lambda self: self.env['crm.team'].sudo()._get_default_team_id(
                                  user_id=self.env.uid), readonly=False, force_save=True)

    def set_salesteam(self):
        for m in self:
            record = self.env['account.payment'].search(
                [(1, '=', 1)])
            print(len(record))
            for n in record:
                user_id = n.env['res.users'].search([('name', '=', n.pos_name_res)], limit=1)
                n.team_id = user_id.sale_team_id.id
                n.payment_user_id = user_id.id



class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

    team_id = fields.Many2one('crm.team', string='Store', oldname='section_id',
                              default=lambda self: self.env['crm.team'].sudo()._get_default_team_id(
                                  user_id=self.env.uid), readonly=False, force_save=True)


class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'

    @api.constrains('user_id')
    def _check_user_id(self):
        for stock in self:
            if stock.user_id.id == False:
                stock.user_id=self.env.uid


    user_warehouse_ids = fields.Many2many('res.users',string='User Warehouse',compute='compute_user_warehouse_ids')

    def compute_user_warehouse_ids(self):
        for rec in self:
            print("rec.picking_type_id.user_ids.ids",rec.picking_type_id.user_ids.ids)
            if rec.picking_type_id.user_ids.ids != []:
                rec.user_warehouse_ids = [(6, 0, rec.picking_type_id.user_ids.ids)]
            else:
                rec.user_warehouse_ids = [(6, 0, [])]


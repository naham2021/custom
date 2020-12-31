from odoo import api, models, fields
from odoo.osv import osv
import odoo.addons.decimal_precision as dp


class AccountInvoice(models.Model):
    _inherit = "account.move"

    pos_order_id = fields.Many2one(comodel_name="pos.order", string="Orders", required=False,compute="_compute_pos_order_id" )

    def _compute_pos_order_id(self):
        for rec in self:
            pos_order = self.env['pos.order'].search([('name', '=',
                                                       rec.ref)],limit=1)

            if pos_order:
                rec.pos_order_id = pos_order.id
            else:
                rec.pos_order_id = []
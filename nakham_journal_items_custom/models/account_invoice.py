from odoo import api, models, fields


class AccountInvoice(models.Model):
    _inherit = "account.move.line"

    group_id = fields.Many2one(related="analytic_account_id.group_id",comodel_name="account.analytic.group", string="Group",store=True, required=False, )
    product_categ = fields.Many2one(related="product_id.categ_id",comodel_name="product.category", string="Product Category",store=True, required=False, )
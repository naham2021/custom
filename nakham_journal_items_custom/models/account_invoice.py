from odoo import api, models, fields
from odoo.osv import osv
import odoo.addons.decimal_precision as dp


class AccountInvoice(models.Model):
    _inherit = "account.move.line"

    group_id = fields.Many2one(related="analytic_account_id.group_id",comodel_name="account.analytic.group", string="Group",store=True, required=False, )
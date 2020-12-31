from odoo import api, models, fields
from odoo.osv import osv
import odoo.addons.decimal_precision as dp


class AccountInvoice(models.Model):
    _inherit = "account.move"

    review = fields.Selection(string="Review", selection=[('to_check', 'To Check'), ('checked', 'Checked'), ],
                              required=False, default="to_check")
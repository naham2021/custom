

from odoo import api, fields, models, tools, _


class AccountPayment(models.Model):
    _inherit = "account.payment"


    review = fields.Selection(string="Review", selection=[('to_check', 'To Check'), ('checked', 'Checked'), ],
                          required=False, default="to_check")
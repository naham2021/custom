

from odoo import api, fields, models, tools, _


class PosOrder(models.Model):
    _inherit = "pos.order"


    review = fields.Selection(string="Review", selection=[('to_check', 'To Check'), ('checked', 'Checked'), ],
                          required=False, default="to_check")
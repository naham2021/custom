

from odoo import api, fields, models, tools, _


class Possession(models.Model):
    _inherit = "pos.session"


    review = fields.Selection(string="Review", selection=[('to_check', 'To Check'), ('checked', 'Checked'), ],
                          required=False, default="to_check")
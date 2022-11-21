
from odoo import models, fields, api


class saleorder(models.Model):
    _inherit = 'sale.order'
    note = fields.Char('Note')
    sale_note = fields.Char('Note')
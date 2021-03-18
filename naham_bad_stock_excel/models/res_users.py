from odoo import fields, models, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    allowed_bad_stock_location_ids = fields.Many2many('stock.location',
                                                      domain=[('usage', '=', 'internal')],
                                                      string="Locations")

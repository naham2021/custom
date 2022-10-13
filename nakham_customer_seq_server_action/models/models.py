from odoo import models, fields, api


class CustomerSeq(models.Model):
    _inherit = 'res.partner'

    def customer_seq_server(self):
        for rec in self:
            if rec.name_seq in [False, 'New']:
                if rec.area_id.id:
                    area_id = self.env['partner.area'].browse(rec.area_id.id)
                    rec.name_seq = str(area_id.code) + str(area_id.next_code_sequence).rjust(5, '0')
                    area_id.next_code_sequence += 1
                    rec.ref = rec.name_seq
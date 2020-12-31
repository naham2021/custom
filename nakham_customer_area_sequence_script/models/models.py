# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def res_partner_area(self):
        for rec in self:
            # if self._context.get('default_customer_rank'):
            if self.customer_rank:
                if rec.area_id:
                    current_area = self.env['partner.area'].sudo().search([('id', '=', rec.area_id.id)])
                    current_area_count = self.env['res.partner'].sudo().search_count([('area_id', '=', rec.area_id.id)])
                    rec.name_seq = str(current_area.code) + '00' + str(current_area_count + 1)

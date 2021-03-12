# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def res_partner_area(self):
        # print(len(self.env['res.partner'].search([('customer_rank', '>', 0)])))
        area_ids = self.env['partner.area'].search([])
        counters = {}
        for area in area_ids:
            if area.code:
                counters[area.id] = 1
        print(counters)
        for rec in self.env['res.partner'].search([('customer_rank', '>', 0)]):
            if rec.area_id:
                rec.name_seq = rec.area_id.code + str(rec.area_id.next_code_sequence).rjust(5, '0')
                rec.area_id.next_code_sequence += 1
            else:
                rec.name_seq = ''

        # for rec in self:
        #     # if self._context.get('default_customer_rank'):
        #     if self.customer_rank:
        #         if rec.area_id:
        #             current_area = self.env['partner.area'].sudo().search([('id', '=', rec.area_id.id)])
        #             current_area_count = self.env['res.partner'].sudo().search_count([('area_id', '=', rec.area_id.id)])
        #             rec.name_seq = str(current_area.code) + '00' + str(current_area_count + 1)

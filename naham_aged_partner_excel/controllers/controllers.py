# -*- coding: utf-8 -*-
# from odoo import http


# class NahamAgedPartnerExcel(http.Controller):
#     @http.route('/naham_aged_partner_excel/naham_aged_partner_excel/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/naham_aged_partner_excel/naham_aged_partner_excel/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('naham_aged_partner_excel.listing', {
#             'root': '/naham_aged_partner_excel/naham_aged_partner_excel',
#             'objects': http.request.env['naham_aged_partner_excel.naham_aged_partner_excel'].search([]),
#         })

#     @http.route('/naham_aged_partner_excel/naham_aged_partner_excel/objects/<model("naham_aged_partner_excel.naham_aged_partner_excel"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('naham_aged_partner_excel.object', {
#             'object': obj
#         })

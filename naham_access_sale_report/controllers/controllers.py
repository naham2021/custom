# -*- coding: utf-8 -*-
# from odoo import http


# class NahamAccessSaleReport(http.Controller):
#     @http.route('/naham_access_sale_report/naham_access_sale_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/naham_access_sale_report/naham_access_sale_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('naham_access_sale_report.listing', {
#             'root': '/naham_access_sale_report/naham_access_sale_report',
#             'objects': http.request.env['naham_access_sale_report.naham_access_sale_report'].search([]),
#         })

#     @http.route('/naham_access_sale_report/naham_access_sale_report/objects/<model("naham_access_sale_report.naham_access_sale_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('naham_access_sale_report.object', {
#             'object': obj
#         })

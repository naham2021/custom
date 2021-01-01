# -*- coding: utf-8 -*-
from odoo import http

# class MagrapiAccountingReports(http.Controller):
#     @http.route('/magrapi_accounting_reports/magrapi_accounting_reports/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/magrapi_accounting_reports/magrapi_accounting_reports/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('magrapi_accounting_reports.listing', {
#             'root': '/magrapi_accounting_reports/magrapi_accounting_reports',
#             'objects': http.request.env['magrapi_accounting_reports.magrapi_accounting_reports'].search([]),
#         })

#     @http.route('/magrapi_accounting_reports/magrapi_accounting_reports/objects/<model("magrapi_accounting_reports.magrapi_accounting_reports"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('magrapi_accounting_reports.object', {
#             'object': obj
#         })
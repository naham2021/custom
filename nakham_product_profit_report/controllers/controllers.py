# -*- coding: utf-8 -*-
# from odoo import http


# class NakhamProductProfitReport(http.Controller):
#     @http.route('/nakham_product_profit_report/nakham_product_profit_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nakham_product_profit_report/nakham_product_profit_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nakham_product_profit_report.listing', {
#             'root': '/nakham_product_profit_report/nakham_product_profit_report',
#             'objects': http.request.env['nakham_product_profit_report.nakham_product_profit_report'].search([]),
#         })

#     @http.route('/nakham_product_profit_report/nakham_product_profit_report/objects/<model("nakham_product_profit_report.nakham_product_profit_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nakham_product_profit_report.object', {
#             'object': obj
#         })

# -*- coding: utf-8 -*-
# from odoo import http


# class NakhamSalesRecordRules(http.Controller):
#     @http.route('/nakham_sales_record_rules/nakham_sales_record_rules/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nakham_sales_record_rules/nakham_sales_record_rules/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nakham_sales_record_rules.listing', {
#             'root': '/nakham_sales_record_rules/nakham_sales_record_rules',
#             'objects': http.request.env['nakham_sales_record_rules.nakham_sales_record_rules'].search([]),
#         })

#     @http.route('/nakham_sales_record_rules/nakham_sales_record_rules/objects/<model("nakham_sales_record_rules.nakham_sales_record_rules"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nakham_sales_record_rules.object', {
#             'object': obj
#         })

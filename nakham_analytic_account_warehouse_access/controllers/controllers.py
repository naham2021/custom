# -*- coding: utf-8 -*-
# from odoo import http


# class NakhamAnalyticAccountWarehouseAccess(http.Controller):
#     @http.route('/nakham_analytic_account_warehouse_access/nakham_analytic_account_warehouse_access/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nakham_analytic_account_warehouse_access/nakham_analytic_account_warehouse_access/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nakham_analytic_account_warehouse_access.listing', {
#             'root': '/nakham_analytic_account_warehouse_access/nakham_analytic_account_warehouse_access',
#             'objects': http.request.env['nakham_analytic_account_warehouse_access.nakham_analytic_account_warehouse_access'].search([]),
#         })

#     @http.route('/nakham_analytic_account_warehouse_access/nakham_analytic_account_warehouse_access/objects/<model("nakham_analytic_account_warehouse_access.nakham_analytic_account_warehouse_access"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nakham_analytic_account_warehouse_access.object', {
#             'object': obj
#         })

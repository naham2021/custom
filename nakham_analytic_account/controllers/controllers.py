# -*- coding: utf-8 -*-
from odoo import http

# class NakhamWarehouseAnalyticAccount(http.Controller):
#     @http.route('/nakham_warehouse_analytic_account/nakham_warehouse_analytic_account/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nakham_warehouse_analytic_account/nakham_warehouse_analytic_account/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nakham_warehouse_analytic_account.listing', {
#             'root': '/nakham_warehouse_analytic_account/nakham_warehouse_analytic_account',
#             'objects': http.request.env['nakham_warehouse_analytic_account.nakham_warehouse_analytic_account'].search([]),
#         })

#     @http.route('/nakham_warehouse_analytic_account/nakham_warehouse_analytic_account/objects/<model("nakham_warehouse_analytic_account.nakham_warehouse_analytic_account"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nakham_warehouse_analytic_account.object', {
#             'object': obj
#         })
# -*- coding: utf-8 -*-
from odoo import http

# class NakhamAdjustAnalytic(http.Controller):
#     @http.route('/nakham_adjust_analytic/nakham_adjust_analytic/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nakham_adjust_analytic/nakham_adjust_analytic/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nakham_adjust_analytic.listing', {
#             'root': '/nakham_adjust_analytic/nakham_adjust_analytic',
#             'objects': http.request.env['nakham_adjust_analytic.nakham_adjust_analytic'].search([]),
#         })

#     @http.route('/nakham_adjust_analytic/nakham_adjust_analytic/objects/<model("nakham_adjust_analytic.nakham_adjust_analytic"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nakham_adjust_analytic.object', {
#             'object': obj
#         })
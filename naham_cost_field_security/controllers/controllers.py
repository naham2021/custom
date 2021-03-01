# -*- coding: utf-8 -*-
# from odoo import http


# class NahamCostFieldSecurity(http.Controller):
#     @http.route('/naham_cost_field_security/naham_cost_field_security/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/naham_cost_field_security/naham_cost_field_security/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('naham_cost_field_security.listing', {
#             'root': '/naham_cost_field_security/naham_cost_field_security',
#             'objects': http.request.env['naham_cost_field_security.naham_cost_field_security'].search([]),
#         })

#     @http.route('/naham_cost_field_security/naham_cost_field_security/objects/<model("naham_cost_field_security.naham_cost_field_security"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('naham_cost_field_security.object', {
#             'object': obj
#         })

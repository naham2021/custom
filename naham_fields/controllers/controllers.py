# -*- coding: utf-8 -*-
# from odoo import http


# class NahamFields(http.Controller):
#     @http.route('/naham_fields/naham_fields/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/naham_fields/naham_fields/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('naham_fields.listing', {
#             'root': '/naham_fields/naham_fields',
#             'objects': http.request.env['naham_fields.naham_fields'].search([]),
#         })

#     @http.route('/naham_fields/naham_fields/objects/<model("naham_fields.naham_fields"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('naham_fields.object', {
#             'object': obj
#         })

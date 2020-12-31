# -*- coding: utf-8 -*-
from odoo import http

# class PosScreenResize(http.Controller):
#     @http.route('/nakham_pos_custom_screen/nakham_pos_custom_screen/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nakham_pos_custom_screen/nakham_pos_custom_screen/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nakham_pos_custom_screen.listing', {
#             'root': '/nakham_pos_custom_screen/nakham_pos_custom_screen',
#             'objects': http.request.env['nakham_pos_custom_screen.nakham_pos_custom_screen'].search([]),
#         })

#     @http.route('/nakham_pos_custom_screen/nakham_pos_custom_screen/objects/<model("nakham_pos_custom_screen.nakham_pos_custom_screen"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nakham_pos_custom_screen.object', {
#             'object': obj
#         })
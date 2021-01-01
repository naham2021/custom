# -*- coding: utf-8 -*-
from odoo import http

# class NakhamPosErrorBase(http.Controller):
#     @http.route('/nakham_pos_error_base/nakham_pos_error_base/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nakham_pos_error_base/nakham_pos_error_base/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nakham_pos_error_base.listing', {
#             'root': '/nakham_pos_error_base/nakham_pos_error_base',
#             'objects': http.request.env['nakham_pos_error_base.nakham_pos_error_base'].search([]),
#         })

#     @http.route('/nakham_pos_error_base/nakham_pos_error_base/objects/<model("nakham_pos_error_base.nakham_pos_error_base"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nakham_pos_error_base.object', {
#             'object': obj
#         })
# -*- coding: utf-8 -*-
from odoo import http

# class NakhamChangeSeq(http.Controller):
#     @http.route('/nakham_change_seq/nakham_change_seq/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nakham_change_seq/nakham_change_seq/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nakham_change_seq.listing', {
#             'root': '/nakham_change_seq/nakham_change_seq',
#             'objects': http.request.env['nakham_change_seq.nakham_change_seq'].search([]),
#         })

#     @http.route('/nakham_change_seq/nakham_change_seq/objects/<model("nakham_change_seq.nakham_change_seq"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nakham_change_seq.object', {
#             'object': obj
#         })
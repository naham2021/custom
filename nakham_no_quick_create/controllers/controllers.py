# -*- coding: utf-8 -*-
# from odoo import http


# class NakhamNoQuickCreate(http.Controller):
#     @http.route('/nakham_no_quick_create/nakham_no_quick_create/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nakham_no_quick_create/nakham_no_quick_create/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nakham_no_quick_create.listing', {
#             'root': '/nakham_no_quick_create/nakham_no_quick_create',
#             'objects': http.request.env['nakham_no_quick_create.nakham_no_quick_create'].search([]),
#         })

#     @http.route('/nakham_no_quick_create/nakham_no_quick_create/objects/<model("nakham_no_quick_create.nakham_no_quick_create"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nakham_no_quick_create.object', {
#             'object': obj
#         })

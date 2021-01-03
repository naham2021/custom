# -*- coding: utf-8 -*-
# from odoo import http


# class NakhamDeleteAnEntryPass(http.Controller):
#     @http.route('/nakham_delete_an_entry_pass/nakham_delete_an_entry_pass/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nakham_delete_an_entry_pass/nakham_delete_an_entry_pass/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nakham_delete_an_entry_pass.listing', {
#             'root': '/nakham_delete_an_entry_pass/nakham_delete_an_entry_pass',
#             'objects': http.request.env['nakham_delete_an_entry_pass.nakham_delete_an_entry_pass'].search([]),
#         })

#     @http.route('/nakham_delete_an_entry_pass/nakham_delete_an_entry_pass/objects/<model("nakham_delete_an_entry_pass.nakham_delete_an_entry_pass"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nakham_delete_an_entry_pass.object', {
#             'object': obj
#         })

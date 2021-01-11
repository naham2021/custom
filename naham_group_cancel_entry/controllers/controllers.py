# -*- coding: utf-8 -*-
# from odoo import http


# class NahamGroupCancelEntry(http.Controller):
#     @http.route('/naham_group_cancel_entry/naham_group_cancel_entry/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/naham_group_cancel_entry/naham_group_cancel_entry/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('naham_group_cancel_entry.listing', {
#             'root': '/naham_group_cancel_entry/naham_group_cancel_entry',
#             'objects': http.request.env['naham_group_cancel_entry.naham_group_cancel_entry'].search([]),
#         })

#     @http.route('/naham_group_cancel_entry/naham_group_cancel_entry/objects/<model("naham_group_cancel_entry.naham_group_cancel_entry"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('naham_group_cancel_entry.object', {
#             'object': obj
#         })

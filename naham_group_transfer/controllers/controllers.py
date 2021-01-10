# -*- coding: utf-8 -*-
# from odoo import http


# class NahamGroupTransfer(http.Controller):
#     @http.route('/naham_group_transfer/naham_group_transfer/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/naham_group_transfer/naham_group_transfer/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('naham_group_transfer.listing', {
#             'root': '/naham_group_transfer/naham_group_transfer',
#             'objects': http.request.env['naham_group_transfer.naham_group_transfer'].search([]),
#         })

#     @http.route('/naham_group_transfer/naham_group_transfer/objects/<model("naham_group_transfer.naham_group_transfer"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('naham_group_transfer.object', {
#             'object': obj
#         })

# -*- coding: utf-8 -*-
from odoo import http

# class NakhamPosBlockNewDelOrder(http.Controller):
#     @http.route('/nakham_pos_block_new_del_order/nakham_pos_block_new_del_order/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nakham_pos_block_new_del_order/nakham_pos_block_new_del_order/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nakham_pos_block_new_del_order.listing', {
#             'root': '/nakham_pos_block_new_del_order/nakham_pos_block_new_del_order',
#             'objects': http.request.env['nakham_pos_block_new_del_order.nakham_pos_block_new_del_order'].search([]),
#         })

#     @http.route('/nakham_pos_block_new_del_order/nakham_pos_block_new_del_order/objects/<model("nakham_pos_block_new_del_order.nakham_pos_block_new_del_order"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nakham_pos_block_new_del_order.object', {
#             'object': obj
#         })
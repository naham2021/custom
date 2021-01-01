# -*- coding: utf-8 -*-
from odoo import http

# class NakhamPosBlockAddCustomer(http.Controller):
#     @http.route('/nakham_pos_block_add_customer/nakham_pos_block_add_customer/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nakham_pos_block_add_customer/nakham_pos_block_add_customer/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nakham_pos_block_add_customer.listing', {
#             'root': '/nakham_pos_block_add_customer/nakham_pos_block_add_customer',
#             'objects': http.request.env['nakham_pos_block_add_customer.nakham_pos_block_add_customer'].search([]),
#         })

#     @http.route('/nakham_pos_block_add_customer/nakham_pos_block_add_customer/objects/<model("nakham_pos_block_add_customer.nakham_pos_block_add_customer"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nakham_pos_block_add_customer.object', {
#             'object': obj
#         })
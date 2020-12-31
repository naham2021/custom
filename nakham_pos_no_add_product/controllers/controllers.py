# -*- coding: utf-8 -*-
from odoo import http

# class NakhamPosNoAddProduct(http.Controller):
#     @http.route('/nakham_pos_no_add_product/nakham_pos_no_add_product/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nakham_pos_no_add_product/nakham_pos_no_add_product/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nakham_pos_no_add_product.listing', {
#             'root': '/nakham_pos_no_add_product/nakham_pos_no_add_product',
#             'objects': http.request.env['nakham_pos_no_add_product.nakham_pos_no_add_product'].search([]),
#         })

#     @http.route('/nakham_pos_no_add_product/nakham_pos_no_add_product/objects/<model("nakham_pos_no_add_product.nakham_pos_no_add_product"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nakham_pos_no_add_product.object', {
#             'object': obj
#         })
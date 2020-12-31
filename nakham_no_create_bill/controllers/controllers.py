# -*- coding: utf-8 -*-
from odoo import http

# class NakhamNoCreateBill(http.Controller):
#     @http.route('/nakham_no_create_bill/nakham_no_create_bill/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nakham_no_create_bill/nakham_no_create_bill/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nakham_no_create_bill.listing', {
#             'root': '/nakham_no_create_bill/nakham_no_create_bill',
#             'objects': http.request.env['nakham_no_create_bill.nakham_no_create_bill'].search([]),
#         })

#     @http.route('/nakham_no_create_bill/nakham_no_create_bill/objects/<model("nakham_no_create_bill.nakham_no_create_bill"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nakham_no_create_bill.object', {
#             'object': obj
#         })
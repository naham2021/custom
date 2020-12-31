# -*- coding: utf-8 -*-
from odoo import http

# class NakhamPosPayment(http.Controller):
#     @http.route('/nakham_pos_payment/nakham_pos_payment/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nakham_pos_payment/nakham_pos_payment/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nakham_pos_payment.listing', {
#             'root': '/nakham_pos_payment/nakham_pos_payment',
#             'objects': http.request.env['nakham_pos_payment.nakham_pos_payment'].search([]),
#         })

#     @http.route('/nakham_pos_payment/nakham_pos_payment/objects/<model("nakham_pos_payment.nakham_pos_payment"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nakham_pos_payment.object', {
#             'object': obj
#         })
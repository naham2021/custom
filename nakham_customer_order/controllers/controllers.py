# -*- coding: utf-8 -*-
from odoo import http

# class TamsahCustomerOrder(http.Controller):
#     @http.route('/tamsah_customer_order/tamsah_customer_order/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tamsah_customer_order/tamsah_customer_order/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tamsah_customer_order.listing', {
#             'root': '/tamsah_customer_order/tamsah_customer_order',
#             'objects': http.request.env['tamsah_customer_order.tamsah_customer_order'].search([]),
#         })

#     @http.route('/tamsah_customer_order/tamsah_customer_order/objects/<model("tamsah_customer_order.tamsah_customer_order"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tamsah_customer_order.object', {
#             'object': obj
#         })
# -*- coding: utf-8 -*-
from odoo import http

# class NakhamRequiredFieldsCustomer(http.Controller):
#     @http.route('/nakham_required_fields_customer/nakham_required_fields_customer/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nakham_required_fields_customer/nakham_required_fields_customer/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nakham_required_fields_customer.listing', {
#             'root': '/nakham_required_fields_customer/nakham_required_fields_customer',
#             'objects': http.request.env['nakham_required_fields_customer.nakham_required_fields_customer'].search([]),
#         })

#     @http.route('/nakham_required_fields_customer/nakham_required_fields_customer/objects/<model("nakham_required_fields_customer.nakham_required_fields_customer"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nakham_required_fields_customer.object', {
#             'object': obj
#         })
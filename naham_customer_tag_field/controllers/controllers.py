# -*- coding: utf-8 -*-
# from odoo import http


# class NahamCustomerTagField(http.Controller):
#     @http.route('/naham_customer_tag_field/naham_customer_tag_field/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/naham_customer_tag_field/naham_customer_tag_field/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('naham_customer_tag_field.listing', {
#             'root': '/naham_customer_tag_field/naham_customer_tag_field',
#             'objects': http.request.env['naham_customer_tag_field.naham_customer_tag_field'].search([]),
#         })

#     @http.route('/naham_customer_tag_field/naham_customer_tag_field/objects/<model("naham_customer_tag_field.naham_customer_tag_field"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('naham_customer_tag_field.object', {
#             'object': obj
#         })

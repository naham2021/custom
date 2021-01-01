# -*- coding: utf-8 -*-
from odoo import http

# class SearchProductsWithSerialNo(http.Controller):
#     @http.route('/search_products_with_serial_no/search_products_with_serial_no/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/search_products_with_serial_no/search_products_with_serial_no/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('search_products_with_serial_no.listing', {
#             'root': '/search_products_with_serial_no/search_products_with_serial_no',
#             'objects': http.request.env['search_products_with_serial_no.search_products_with_serial_no'].search([]),
#         })

#     @http.route('/search_products_with_serial_no/search_products_with_serial_no/objects/<model("search_products_with_serial_no.search_products_with_serial_no"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('search_products_with_serial_no.object', {
#             'object': obj
#         })
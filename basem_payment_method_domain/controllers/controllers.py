# -*- coding: utf-8 -*-
from odoo import http

# class BasemDomainProductByVendor(http.Controller):
#     @http.route('/basem_domain_product_by_vendor/basem_domain_product_by_vendor/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/basem_domain_product_by_vendor/basem_domain_product_by_vendor/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('basem_domain_product_by_vendor.listing', {
#             'root': '/basem_domain_product_by_vendor/basem_domain_product_by_vendor',
#             'objects': http.request.env['basem_domain_product_by_vendor.basem_domain_product_by_vendor'].search([]),
#         })

#     @http.route('/basem_domain_product_by_vendor/basem_domain_product_by_vendor/objects/<model("basem_domain_product_by_vendor.basem_domain_product_by_vendor"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('basem_domain_product_by_vendor.object', {
#             'object': obj
#         })
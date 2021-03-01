# -*- coding: utf-8 -*-
# from odoo import http


# class NahamInvoicePrintSecurity(http.Controller):
#     @http.route('/naham_invoice_print_security/naham_invoice_print_security/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/naham_invoice_print_security/naham_invoice_print_security/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('naham_invoice_print_security.listing', {
#             'root': '/naham_invoice_print_security/naham_invoice_print_security',
#             'objects': http.request.env['naham_invoice_print_security.naham_invoice_print_security'].search([]),
#         })

#     @http.route('/naham_invoice_print_security/naham_invoice_print_security/objects/<model("naham_invoice_print_security.naham_invoice_print_security"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('naham_invoice_print_security.object', {
#             'object': obj
#         })

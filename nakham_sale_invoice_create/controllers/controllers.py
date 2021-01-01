# -*- coding: utf-8 -*-
# from odoo import http


# class NakhamSaleInvoiceCreate(http.Controller):
#     @http.route('/nakham_sale_invoice_create/nakham_sale_invoice_create/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nakham_sale_invoice_create/nakham_sale_invoice_create/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nakham_sale_invoice_create.listing', {
#             'root': '/nakham_sale_invoice_create/nakham_sale_invoice_create',
#             'objects': http.request.env['nakham_sale_invoice_create.nakham_sale_invoice_create'].search([]),
#         })

#     @http.route('/nakham_sale_invoice_create/nakham_sale_invoice_create/objects/<model("nakham_sale_invoice_create.nakham_sale_invoice_create"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nakham_sale_invoice_create.object', {
#             'object': obj
#         })

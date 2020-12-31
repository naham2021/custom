# -*- coding: utf-8 -*-
# from odoo import http


# class NakhamInvoiceLineMenu(http.Controller):
#     @http.route('/nakham_invoice_line_menu/nakham_invoice_line_menu/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nakham_invoice_line_menu/nakham_invoice_line_menu/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nakham_invoice_line_menu.listing', {
#             'root': '/nakham_invoice_line_menu/nakham_invoice_line_menu',
#             'objects': http.request.env['nakham_invoice_line_menu.nakham_invoice_line_menu'].search([]),
#         })

#     @http.route('/nakham_invoice_line_menu/nakham_invoice_line_menu/objects/<model("nakham_invoice_line_menu.nakham_invoice_line_menu"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nakham_invoice_line_menu.object', {
#             'object': obj
#         })

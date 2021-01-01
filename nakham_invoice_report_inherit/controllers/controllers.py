# -*- coding: utf-8 -*-
# from odoo import http


# class NakhamInvoiceReportInherit(http.Controller):
#     @http.route('/nakham_invoice_report_inherit/nakham_invoice_report_inherit/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nakham_invoice_report_inherit/nakham_invoice_report_inherit/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nakham_invoice_report_inherit.listing', {
#             'root': '/nakham_invoice_report_inherit/nakham_invoice_report_inherit',
#             'objects': http.request.env['nakham_invoice_report_inherit.nakham_invoice_report_inherit'].search([]),
#         })

#     @http.route('/nakham_invoice_report_inherit/nakham_invoice_report_inherit/objects/<model("nakham_invoice_report_inherit.nakham_invoice_report_inherit"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nakham_invoice_report_inherit.object', {
#             'object': obj
#         })

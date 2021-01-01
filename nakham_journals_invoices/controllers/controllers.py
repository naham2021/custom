# -*- coding: utf-8 -*-
from odoo import http

# class NakhamJournalsInvoices(http.Controller):
#     @http.route('/nakham_journals_invoices/nakham_journals_invoices/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nakham_journals_invoices/nakham_journals_invoices/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nakham_journals_invoices.listing', {
#             'root': '/nakham_journals_invoices/nakham_journals_invoices',
#             'objects': http.request.env['nakham_journals_invoices.nakham_journals_invoices'].search([]),
#         })

#     @http.route('/nakham_journals_invoices/nakham_journals_invoices/objects/<model("nakham_journals_invoices.nakham_journals_invoices"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nakham_journals_invoices.object', {
#             'object': obj
#         })
# -*- coding: utf-8 -*-
# from odoo import http


# class NakhamGroupToDraftInvoice(http.Controller):
#     @http.route('/nakham_group_to_draft_invoice/nakham_group_to_draft_invoice/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nakham_group_to_draft_invoice/nakham_group_to_draft_invoice/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nakham_group_to_draft_invoice.listing', {
#             'root': '/nakham_group_to_draft_invoice/nakham_group_to_draft_invoice',
#             'objects': http.request.env['nakham_group_to_draft_invoice.nakham_group_to_draft_invoice'].search([]),
#         })

#     @http.route('/nakham_group_to_draft_invoice/nakham_group_to_draft_invoice/objects/<model("nakham_group_to_draft_invoice.nakham_group_to_draft_invoice"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nakham_group_to_draft_invoice.object', {
#             'object': obj
#         })

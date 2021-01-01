# -*- coding: utf-8 -*-
from odoo import http

# class NakhamPosLinkInvoice(http.Controller):
#     @http.route('/nakham_pos_link_invoice/nakham_pos_link_invoice/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nakham_pos_link_invoice/nakham_pos_link_invoice/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nakham_pos_link_invoice.listing', {
#             'root': '/nakham_pos_link_invoice/nakham_pos_link_invoice',
#             'objects': http.request.env['nakham_pos_link_invoice.nakham_pos_link_invoice'].search([]),
#         })

#     @http.route('/nakham_pos_link_invoice/nakham_pos_link_invoice/objects/<model("nakham_pos_link_invoice.nakham_pos_link_invoice"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nakham_pos_link_invoice.object', {
#             'object': obj
#         })
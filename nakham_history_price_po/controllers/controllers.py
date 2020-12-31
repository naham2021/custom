# -*- coding: utf-8 -*-
from odoo import http

# class NakhamHistoryPricePo(http.Controller):
#     @http.route('/nakham_history_price_po/nakham_history_price_po/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nakham_history_price_po/nakham_history_price_po/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nakham_history_price_po.listing', {
#             'root': '/nakham_history_price_po/nakham_history_price_po',
#             'objects': http.request.env['nakham_history_price_po.nakham_history_price_po'].search([]),
#         })

#     @http.route('/nakham_history_price_po/nakham_history_price_po/objects/<model("nakham_history_price_po.nakham_history_price_po"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nakham_history_price_po.object', {
#             'object': obj
#         })
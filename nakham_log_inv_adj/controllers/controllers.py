# -*- coding: utf-8 -*-
# from odoo import http


# class NakhamLogInvAdj(http.Controller):
#     @http.route('/nakham_log_inv_adj/nakham_log_inv_adj/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nakham_log_inv_adj/nakham_log_inv_adj/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nakham_log_inv_adj.listing', {
#             'root': '/nakham_log_inv_adj/nakham_log_inv_adj',
#             'objects': http.request.env['nakham_log_inv_adj.nakham_log_inv_adj'].search([]),
#         })

#     @http.route('/nakham_log_inv_adj/nakham_log_inv_adj/objects/<model("nakham_log_inv_adj.nakham_log_inv_adj"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nakham_log_inv_adj.object', {
#             'object': obj
#         })

# -*- coding: utf-8 -*-
from odoo import http

# class NakhamDomainActionTransfer(http.Controller):
#     @http.route('/nakham_domain_action_transfer/nakham_domain_action_transfer/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nakham_domain_action_transfer/nakham_domain_action_transfer/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nakham_domain_action_transfer.listing', {
#             'root': '/nakham_domain_action_transfer/nakham_domain_action_transfer',
#             'objects': http.request.env['nakham_domain_action_transfer.nakham_domain_action_transfer'].search([]),
#         })

#     @http.route('/nakham_domain_action_transfer/nakham_domain_action_transfer/objects/<model("nakham_domain_action_transfer.nakham_domain_action_transfer"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nakham_domain_action_transfer.object', {
#             'object': obj
#         })
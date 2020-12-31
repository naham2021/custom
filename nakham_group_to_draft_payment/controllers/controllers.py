# -*- coding: utf-8 -*-
# from odoo import http


# class NakhamGroupToDraftPayment(http.Controller):
#     @http.route('/nakham_group_to_draft_payment/nakham_group_to_draft_payment/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nakham_group_to_draft_payment/nakham_group_to_draft_payment/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nakham_group_to_draft_payment.listing', {
#             'root': '/nakham_group_to_draft_payment/nakham_group_to_draft_payment',
#             'objects': http.request.env['nakham_group_to_draft_payment.nakham_group_to_draft_payment'].search([]),
#         })

#     @http.route('/nakham_group_to_draft_payment/nakham_group_to_draft_payment/objects/<model("nakham_group_to_draft_payment.nakham_group_to_draft_payment"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nakham_group_to_draft_payment.object', {
#             'object': obj
#         })

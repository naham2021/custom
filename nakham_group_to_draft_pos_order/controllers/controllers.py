# -*- coding: utf-8 -*-
# from odoo import http


# class NakhamGroupToDraftPosOrder(http.Controller):
#     @http.route('/nakham_group_to_draft_pos_order/nakham_group_to_draft_pos_order/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nakham_group_to_draft_pos_order/nakham_group_to_draft_pos_order/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nakham_group_to_draft_pos_order.listing', {
#             'root': '/nakham_group_to_draft_pos_order/nakham_group_to_draft_pos_order',
#             'objects': http.request.env['nakham_group_to_draft_pos_order.nakham_group_to_draft_pos_order'].search([]),
#         })

#     @http.route('/nakham_group_to_draft_pos_order/nakham_group_to_draft_pos_order/objects/<model("nakham_group_to_draft_pos_order.nakham_group_to_draft_pos_order"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nakham_group_to_draft_pos_order.object', {
#             'object': obj
#         })

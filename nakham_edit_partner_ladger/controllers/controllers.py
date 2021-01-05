# -*- coding: utf-8 -*-
# from odoo import http


# class NakhamEditPartnerLadger(http.Controller):
#     @http.route('/nakham_edit_partner_ladger/nakham_edit_partner_ladger/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nakham_edit_partner_ladger/nakham_edit_partner_ladger/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nakham_edit_partner_ladger.listing', {
#             'root': '/nakham_edit_partner_ladger/nakham_edit_partner_ladger',
#             'objects': http.request.env['nakham_edit_partner_ladger.nakham_edit_partner_ladger'].search([]),
#         })

#     @http.route('/nakham_edit_partner_ladger/nakham_edit_partner_ladger/objects/<model("nakham_edit_partner_ladger.nakham_edit_partner_ladger"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nakham_edit_partner_ladger.object', {
#             'object': obj
#         })

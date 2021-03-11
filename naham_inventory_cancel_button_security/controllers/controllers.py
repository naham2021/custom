# -*- coding: utf-8 -*-
# from odoo import http


# class NahamInventoryCancelButtonSecurity(http.Controller):
#     @http.route('/naham_inventory_cancel_button_security/naham_inventory_cancel_button_security/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/naham_inventory_cancel_button_security/naham_inventory_cancel_button_security/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('naham_inventory_cancel_button_security.listing', {
#             'root': '/naham_inventory_cancel_button_security/naham_inventory_cancel_button_security',
#             'objects': http.request.env['naham_inventory_cancel_button_security.naham_inventory_cancel_button_security'].search([]),
#         })

#     @http.route('/naham_inventory_cancel_button_security/naham_inventory_cancel_button_security/objects/<model("naham_inventory_cancel_button_security.naham_inventory_cancel_button_security"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('naham_inventory_cancel_button_security.object', {
#             'object': obj
#         })

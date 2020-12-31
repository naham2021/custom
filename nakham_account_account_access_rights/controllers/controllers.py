# -*- coding: utf-8 -*-
# from odoo import http


# class NakhamAccountAccountAccessRights(http.Controller):
#     @http.route('/nakham_account_account_access_rights/nakham_account_account_access_rights/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nakham_account_account_access_rights/nakham_account_account_access_rights/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nakham_account_account_access_rights.listing', {
#             'root': '/nakham_account_account_access_rights/nakham_account_account_access_rights',
#             'objects': http.request.env['nakham_account_account_access_rights.nakham_account_account_access_rights'].search([]),
#         })

#     @http.route('/nakham_account_account_access_rights/nakham_account_account_access_rights/objects/<model("nakham_account_account_access_rights.nakham_account_account_access_rights"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nakham_account_account_access_rights.object', {
#             'object': obj
#         })

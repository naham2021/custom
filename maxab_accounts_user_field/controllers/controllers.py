# -*- coding: utf-8 -*-
from odoo import http

# class MaxabAccountsUserField(http.Controller):
#     @http.route('/maxab_accounts_user_field/maxab_accounts_user_field/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/maxab_accounts_user_field/maxab_accounts_user_field/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('maxab_accounts_user_field.listing', {
#             'root': '/maxab_accounts_user_field/maxab_accounts_user_field',
#             'objects': http.request.env['maxab_accounts_user_field.maxab_accounts_user_field'].search([]),
#         })

#     @http.route('/maxab_accounts_user_field/maxab_accounts_user_field/objects/<model("maxab_accounts_user_field.maxab_accounts_user_field"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('maxab_accounts_user_field.object', {
#             'object': obj
#         })
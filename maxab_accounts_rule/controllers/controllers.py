# -*- coding: utf-8 -*-
from odoo import http

# class MaxabAccountsRule(http.Controller):
#     @http.route('/maxab_accounts_rule/maxab_accounts_rule/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/maxab_accounts_rule/maxab_accounts_rule/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('maxab_accounts_rule.listing', {
#             'root': '/maxab_accounts_rule/maxab_accounts_rule',
#             'objects': http.request.env['maxab_accounts_rule.maxab_accounts_rule'].search([]),
#         })

#     @http.route('/maxab_accounts_rule/maxab_accounts_rule/objects/<model("maxab_accounts_rule.maxab_accounts_rule"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('maxab_accounts_rule.object', {
#             'object': obj
#         })
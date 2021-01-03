# -*- coding: utf-8 -*-
from odoo import http

# class NakhamSalesTeamRule(http.Controller):
#     @http.route('/nakham_sales_team_rule/nakham_sales_team_rule/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nakham_sales_team_rule/nakham_sales_team_rule/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nakham_sales_team_rule.listing', {
#             'root': '/nakham_sales_team_rule/nakham_sales_team_rule',
#             'objects': http.request.env['nakham_sales_team_rule.nakham_sales_team_rule'].search([]),
#         })

#     @http.route('/nakham_sales_team_rule/nakham_sales_team_rule/objects/<model("nakham_sales_team_rule.nakham_sales_team_rule"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nakham_sales_team_rule.object', {
#             'object': obj
#         })
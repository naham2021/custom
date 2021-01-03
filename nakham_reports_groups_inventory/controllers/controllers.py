# -*- coding: utf-8 -*-
# from odoo import http


# class NakhamReportsGroupsInventory(http.Controller):
#     @http.route('/nakham_reports_groups_inventory/nakham_reports_groups_inventory/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nakham_reports_groups_inventory/nakham_reports_groups_inventory/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nakham_reports_groups_inventory.listing', {
#             'root': '/nakham_reports_groups_inventory/nakham_reports_groups_inventory',
#             'objects': http.request.env['nakham_reports_groups_inventory.nakham_reports_groups_inventory'].search([]),
#         })

#     @http.route('/nakham_reports_groups_inventory/nakham_reports_groups_inventory/objects/<model("nakham_reports_groups_inventory.nakham_reports_groups_inventory"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nakham_reports_groups_inventory.object', {
#             'object': obj
#         })

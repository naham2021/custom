# -*- coding: utf-8 -*-
# from odoo import http


# class NakhamInventoryScrapCancelGroups(http.Controller):
#     @http.route('/nakham_inventory_scrap_cancel_groups/nakham_inventory_scrap_cancel_groups/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nakham_inventory_scrap_cancel_groups/nakham_inventory_scrap_cancel_groups/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nakham_inventory_scrap_cancel_groups.listing', {
#             'root': '/nakham_inventory_scrap_cancel_groups/nakham_inventory_scrap_cancel_groups',
#             'objects': http.request.env['nakham_inventory_scrap_cancel_groups.nakham_inventory_scrap_cancel_groups'].search([]),
#         })

#     @http.route('/nakham_inventory_scrap_cancel_groups/nakham_inventory_scrap_cancel_groups/objects/<model("nakham_inventory_scrap_cancel_groups.nakham_inventory_scrap_cancel_groups"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nakham_inventory_scrap_cancel_groups.object', {
#             'object': obj
#         })

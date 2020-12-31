# -*- coding: utf-8 -*-
from odoo import http

# class NakhamAssetAction(http.Controller):
#     @http.route('/nakham_asset_action/nakham_asset_action/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nakham_asset_action/nakham_asset_action/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nakham_asset_action.listing', {
#             'root': '/nakham_asset_action/nakham_asset_action',
#             'objects': http.request.env['nakham_asset_action.nakham_asset_action'].search([]),
#         })

#     @http.route('/nakham_asset_action/nakham_asset_action/objects/<model("nakham_asset_action.nakham_asset_action"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nakham_asset_action.object', {
#             'object': obj
#         })
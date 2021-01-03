# -*- coding: utf-8 -*-
from odoo import http

# class SvAssetConfirm(http.Controller):
#     @http.route('/sv_asset_confirm/sv_asset_confirm/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sv_asset_confirm/sv_asset_confirm/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sv_asset_confirm.listing', {
#             'root': '/sv_asset_confirm/sv_asset_confirm',
#             'objects': http.request.env['sv_asset_confirm.sv_asset_confirm'].search([]),
#         })

#     @http.route('/sv_asset_confirm/sv_asset_confirm/objects/<model("sv_asset_confirm.sv_asset_confirm"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sv_asset_confirm.object', {
#             'object': obj
#         })
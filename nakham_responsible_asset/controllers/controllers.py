# -*- coding: utf-8 -*-
# from odoo import http


# class NakhamResponsibleAsset(http.Controller):
#     @http.route('/nakham_responsible_asset/nakham_responsible_asset/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nakham_responsible_asset/nakham_responsible_asset/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nakham_responsible_asset.listing', {
#             'root': '/nakham_responsible_asset/nakham_responsible_asset',
#             'objects': http.request.env['nakham_responsible_asset.nakham_responsible_asset'].search([]),
#         })

#     @http.route('/nakham_responsible_asset/nakham_responsible_asset/objects/<model("nakham_responsible_asset.nakham_responsible_asset"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nakham_responsible_asset.object', {
#             'object': obj
#         })

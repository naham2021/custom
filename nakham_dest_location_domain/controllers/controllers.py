# -*- coding: utf-8 -*-
from odoo import http

# class TradelineDestLocationDomain(http.Controller):
#     @http.route('/tradeline_dest_location_domain/tradeline_dest_location_domain/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tradeline_dest_location_domain/tradeline_dest_location_domain/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tradeline_dest_location_domain.listing', {
#             'root': '/tradeline_dest_location_domain/tradeline_dest_location_domain',
#             'objects': http.request.env['tradeline_dest_location_domain.tradeline_dest_location_domain'].search([]),
#         })

#     @http.route('/tradeline_dest_location_domain/tradeline_dest_location_domain/objects/<model("tradeline_dest_location_domain.tradeline_dest_location_domain"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tradeline_dest_location_domain.object', {
#             'object': obj
#         })
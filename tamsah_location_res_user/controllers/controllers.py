# -*- coding: utf-8 -*-
from odoo import http

# class TamsahLocationResUser(http.Controller):
#     @http.route('/tamsah_location_res_user/tamsah_location_res_user/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tamsah_location_res_user/tamsah_location_res_user/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tamsah_location_res_user.listing', {
#             'root': '/tamsah_location_res_user/tamsah_location_res_user',
#             'objects': http.request.env['tamsah_location_res_user.tamsah_location_res_user'].search([]),
#         })

#     @http.route('/tamsah_location_res_user/tamsah_location_res_user/objects/<model("tamsah_location_res_user.tamsah_location_res_user"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tamsah_location_res_user.object', {
#             'object': obj
#         })
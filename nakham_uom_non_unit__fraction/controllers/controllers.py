# -*- coding: utf-8 -*-
from odoo import http

# class NakhamUomNonUnitFraction(http.Controller):
#     @http.route('/nakham_uom_non_unit__fraction/nakham_uom_non_unit__fraction/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nakham_uom_non_unit__fraction/nakham_uom_non_unit__fraction/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nakham_uom_non_unit__fraction.listing', {
#             'root': '/nakham_uom_non_unit__fraction/nakham_uom_non_unit__fraction',
#             'objects': http.request.env['nakham_uom_non_unit__fraction.nakham_uom_non_unit__fraction'].search([]),
#         })

#     @http.route('/nakham_uom_non_unit__fraction/nakham_uom_non_unit__fraction/objects/<model("nakham_uom_non_unit__fraction.nakham_uom_non_unit__fraction"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nakham_uom_non_unit__fraction.object', {
#             'object': obj
#         })
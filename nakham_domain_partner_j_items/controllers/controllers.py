# -*- coding: utf-8 -*-
# from odoo import http


# class NakhamDomainPartnerJItems(http.Controller):
#     @http.route('/nakham_domain_partner_j_items/nakham_domain_partner_j_items/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nakham_domain_partner_j_items/nakham_domain_partner_j_items/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nakham_domain_partner_j_items.listing', {
#             'root': '/nakham_domain_partner_j_items/nakham_domain_partner_j_items',
#             'objects': http.request.env['nakham_domain_partner_j_items.nakham_domain_partner_j_items'].search([]),
#         })

#     @http.route('/nakham_domain_partner_j_items/nakham_domain_partner_j_items/objects/<model("nakham_domain_partner_j_items.nakham_domain_partner_j_items"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nakham_domain_partner_j_items.object', {
#             'object': obj
#         })

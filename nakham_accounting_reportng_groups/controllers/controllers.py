# -*- coding: utf-8 -*-
# from odoo import http


# class NakhamAccountingReportngGroups(http.Controller):
#     @http.route('/nakham_accounting_reportng_groups/nakham_accounting_reportng_groups/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nakham_accounting_reportng_groups/nakham_accounting_reportng_groups/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nakham_accounting_reportng_groups.listing', {
#             'root': '/nakham_accounting_reportng_groups/nakham_accounting_reportng_groups',
#             'objects': http.request.env['nakham_accounting_reportng_groups.nakham_accounting_reportng_groups'].search([]),
#         })

#     @http.route('/nakham_accounting_reportng_groups/nakham_accounting_reportng_groups/objects/<model("nakham_accounting_reportng_groups.nakham_accounting_reportng_groups"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nakham_accounting_reportng_groups.object', {
#             'object': obj
#         })

# -*- coding: utf-8 -*-
# from odoo import http


# class NahamReverseTranserWizard(http.Controller):
#     @http.route('/naham_reverse_transer_wizard/naham_reverse_transer_wizard/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/naham_reverse_transer_wizard/naham_reverse_transer_wizard/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('naham_reverse_transer_wizard.listing', {
#             'root': '/naham_reverse_transer_wizard/naham_reverse_transer_wizard',
#             'objects': http.request.env['naham_reverse_transer_wizard.naham_reverse_transer_wizard'].search([]),
#         })

#     @http.route('/naham_reverse_transer_wizard/naham_reverse_transer_wizard/objects/<model("naham_reverse_transer_wizard.naham_reverse_transer_wizard"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('naham_reverse_transer_wizard.object', {
#             'object': obj
#         })

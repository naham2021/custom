# -*- coding: utf-8 -*-
# from odoo import http


# class NakhamJournalOperationRules(http.Controller):
#     @http.route('/nakham_journal_operation_rules/nakham_journal_operation_rules/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nakham_journal_operation_rules/nakham_journal_operation_rules/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nakham_journal_operation_rules.listing', {
#             'root': '/nakham_journal_operation_rules/nakham_journal_operation_rules',
#             'objects': http.request.env['nakham_journal_operation_rules.nakham_journal_operation_rules'].search([]),
#         })

#     @http.route('/nakham_journal_operation_rules/nakham_journal_operation_rules/objects/<model("nakham_journal_operation_rules.nakham_journal_operation_rules"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nakham_journal_operation_rules.object', {
#             'object': obj
#         })

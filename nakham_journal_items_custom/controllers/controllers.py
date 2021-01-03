# -*- coding: utf-8 -*-
from odoo import http

# class NakhamJournalItemsCustom(http.Controller):
#     @http.route('/nakham_journal_items_custom/nakham_journal_items_custom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nakham_journal_items_custom/nakham_journal_items_custom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nakham_journal_items_custom.listing', {
#             'root': '/nakham_journal_items_custom/nakham_journal_items_custom',
#             'objects': http.request.env['nakham_journal_items_custom.nakham_journal_items_custom'].search([]),
#         })

#     @http.route('/nakham_journal_items_custom/nakham_journal_items_custom/objects/<model("nakham_journal_items_custom.nakham_journal_items_custom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nakham_journal_items_custom.object', {
#             'object': obj
#         })
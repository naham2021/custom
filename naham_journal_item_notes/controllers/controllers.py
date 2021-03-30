# -*- coding: utf-8 -*-
# from odoo import http


# class NahamJournalItemNotes(http.Controller):
#     @http.route('/naham_journal_item_notes/naham_journal_item_notes/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/naham_journal_item_notes/naham_journal_item_notes/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('naham_journal_item_notes.listing', {
#             'root': '/naham_journal_item_notes/naham_journal_item_notes',
#             'objects': http.request.env['naham_journal_item_notes.naham_journal_item_notes'].search([]),
#         })

#     @http.route('/naham_journal_item_notes/naham_journal_item_notes/objects/<model("naham_journal_item_notes.naham_journal_item_notes"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('naham_journal_item_notes.object', {
#             'object': obj
#         })

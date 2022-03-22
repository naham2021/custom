# -*- coding: utf-8 -*-
# from odoo import http


# class NahamPartnerJournalItems(http.Controller):
#     @http.route('/naham_partner_journal_items/naham_partner_journal_items/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/naham_partner_journal_items/naham_partner_journal_items/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('naham_partner_journal_items.listing', {
#             'root': '/naham_partner_journal_items/naham_partner_journal_items',
#             'objects': http.request.env['naham_partner_journal_items.naham_partner_journal_items'].search([]),
#         })

#     @http.route('/naham_partner_journal_items/naham_partner_journal_items/objects/<model("naham_partner_journal_items.naham_partner_journal_items"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('naham_partner_journal_items.object', {
#             'object': obj
#         })

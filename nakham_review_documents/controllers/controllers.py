# -*- coding: utf-8 -*-
# from odoo import http


# class NakhamReviewDocuments(http.Controller):
#     @http.route('/nakham_review_documents/nakham_review_documents/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nakham_review_documents/nakham_review_documents/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nakham_review_documents.listing', {
#             'root': '/nakham_review_documents/nakham_review_documents',
#             'objects': http.request.env['nakham_review_documents.nakham_review_documents'].search([]),
#         })

#     @http.route('/nakham_review_documents/nakham_review_documents/objects/<model("nakham_review_documents.nakham_review_documents"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nakham_review_documents.object', {
#             'object': obj
#         })

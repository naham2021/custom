# -*- coding: utf-8 -*-
# from odoo import http


# class NahamPaymentWidget(http.Controller):
#     @http.route('/naham_payment_widget/naham_payment_widget/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/naham_payment_widget/naham_payment_widget/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('naham_payment_widget.listing', {
#             'root': '/naham_payment_widget/naham_payment_widget',
#             'objects': http.request.env['naham_payment_widget.naham_payment_widget'].search([]),
#         })

#     @http.route('/naham_payment_widget/naham_payment_widget/objects/<model("naham_payment_widget.naham_payment_widget"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('naham_payment_widget.object', {
#             'object': obj
#         })

# -*- coding: utf-8 -*-
# from odoo import http


# class NakhamCategoryGroupBy(http.Controller):
#     @http.route('/nakham_category_group_by/nakham_category_group_by/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nakham_category_group_by/nakham_category_group_by/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nakham_category_group_by.listing', {
#             'root': '/nakham_category_group_by/nakham_category_group_by',
#             'objects': http.request.env['nakham_category_group_by.nakham_category_group_by'].search([]),
#         })

#     @http.route('/nakham_category_group_by/nakham_category_group_by/objects/<model("nakham_category_group_by.nakham_category_group_by"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nakham_category_group_by.object', {
#             'object': obj
#         })

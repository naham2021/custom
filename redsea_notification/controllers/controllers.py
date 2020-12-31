# -*- coding: utf-8 -*-
from odoo import http

# class RedseaNotification(http.Controller):
#     @http.route('/redsea_notification/redsea_notification/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/redsea_notification/redsea_notification/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('redsea_notification.listing', {
#             'root': '/redsea_notification/redsea_notification',
#             'objects': http.request.env['redsea_notification.redsea_notification'].search([]),
#         })

#     @http.route('/redsea_notification/redsea_notification/objects/<model("redsea_notification.redsea_notification"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('redsea_notification.object', {
#             'object': obj
#         })
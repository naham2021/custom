# -*- coding: utf-8 -*-

import math

from odoo import http, _, fields,models
from odoo.http import request
from datetime import datetime, timedelta
from odoo.exceptions import UserError
# from odoo.addons.website_portal.controllers.main import website_account
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager

# class website_account(website_account):
class CustomerPortal(CustomerPortal):
    
    def _prepare_portal_layout_values(self):
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>Context",http.request.env.context)
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        employee = request.env.user.employee_id.id
        excuse = request.env['hr.excuse']
        excuse_count = excuse.sudo().search_count([
        ('employee_id', 'in', [employee,]),
        
          ])
        print(">>>>>>>>>>>>>>>>H Count ",excuse_count)
        values.update({
        'excuse_count': excuse_count,
        })
        return values
    
    @http.route(['/my/excuse_request', '/my/excuse_request/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_excuse_request(self, page=1, sortby=None, **kw):
        if not request.env.user.has_group('centione_portal_hr_self_service.group_portal_excuse'):
            # return request.render("odoo_timesheet_portal_user_employee.not_allowed_leave_request")
            return request.render("centione_portal_hr_self_service.not_allowed_excuse_request")
        response = super(CustomerPortal, self)
        values = self._prepare_portal_layout_values()
        excuse_obj = http.request.env['hr.excuse']
        domain = [
            ('employee_id', 'in', [request.env.user.employee_id.id,]),
            
        ]
        # count for pager
        excuse_count = http.request.env['hr.excuse'].sudo().search_count(domain)

        pager = portal_pager(
            url="/my/leaves",
            total=excuse_count,
            page=page,
            step=self._items_per_page
        )
        sortings = {
            'date': {'label': _('Newest'), 'order': 'state,start_date desc'},
        }
        
        order = sortings.get(sortby, sortings['date'])['order']
        
        # content according to pager and archive selected
        excuses = excuse_obj.sudo().search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        domain = [
            ('employee_id.coach_id.user_id', 'in', [request.env.user.id,]),
            
        ]
        excuses_coach = excuse_obj.sudo().search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        
        domain = [
            ('employee_id.parent_id.user_id', 'in', [request.env.user.id,]),
            
        ]
        excuses_manager = excuse_obj.sudo().search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        
        values.update({
            'excuses': excuses,
            'excuses_coach':excuses_coach,
            'excuses_manager':excuses_manager,
            'page_name': 'Excuses',
            'sortings' : sortings,
            'sortby': sortby,
            'pager': pager,
            'default_url': '/my/excuse_request',
        })
        return request.render("centione_portal_hr_self_service.display_excuses", values)


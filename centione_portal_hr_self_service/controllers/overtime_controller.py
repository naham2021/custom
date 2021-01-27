# -*- coding: utf-8 -*-

import math

from odoo import http, _, fields,models
from odoo.http import request
from datetime import datetime, timedelta
from odoo.exceptions import UserError
# from odoo.addons.website_portal.controllers.main import website_account
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager
from odoo.osv.expression import OR

# class website_account(website_account):
class CustomerPortal(CustomerPortal):
    
    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        employee = request.env.user.employee_id.id
        over_time = request.env['over.time']
        over_time_count = over_time.sudo().search_count([
        ('employee_id', 'in', [employee,]),
        
          ])
        values.update({
        'over_time_count': over_time_count,
        })
        return values
    
    @http.route(['/my/over_time_request', '/my/over_time_request/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_over_time_request(self, page=1, sortby=None, search=None, search_in='all',**kw):
        if not request.env.user.has_group('centione_portal_hr_self_service.group_portal_over_time'):
            # return request.render("odoo_timesheet_portal_user_employee.not_allowed_leave_request")
            return request.render("centione_portal_hr_self_service.not_allowed_over_time_request")
        response = super(CustomerPortal, self)
        values = self._prepare_portal_layout_values()
        over_time_obj = http.request.env['over.time']
        domain = [
            ('employee_id', 'in', [request.env.user.employee_id.id,]),
            
        ]
        # count for pager
        over_time_count = http.request.env['over.time'].sudo().search_count(domain)

        pager = portal_pager(
            url="/my/leaves",
            total=over_time_count,
            page=page,
            step=self._items_per_page
        )
        sortings = {
            'date': {'label': _('Newest'), 'order': 'date_from desc'},
        }
        searchbar_sortings = {
            'date': {'label': _('Exeuce Date'), 'order': 'date_from desc'},
            
             'state': {'label': _('Status'), 'order': 'state'},
        }
        searchbar_input = {
            'input': {'label': _('Exeuce Date'), 'input': 'date_from'},
            
             'state': {'label': _('Status'), 'order': 'state'},
        }
        searchbar_inputs = {
            'holiday_type': {'input': 'holiday_type', 'label': _('Search in Holiday Type')},
            'state': {'input': 'state', 'label': _('Search in State')},
            'all': {'input': 'all', 'label': _('Search in All')},
        }
        domain_mng = []
        domain_ch=[]
        if search and search_in:
            search_domain = []
            if search_in in ('state', 'all'):
                search_domain = OR([search_domain, [('state', 'ilike', search),]])
            if search_in in ('holiday_type', 'all'):
                search_domain = OR([search_domain, [('holiday_type', 'ilike', search),]])
        
            domain += search_domain
            domain_ch += search_domain
            domain_mng += search_domain

        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']
        
        # content according to pager and archive selected
        over_times = over_time_obj.sudo().search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        domain_ch += [
            ('employee_id.coach_id.user_id', 'in', [request.env.user.id,]),
            
        ]
        
        over_times_coach = over_time_obj.sudo().search(domain_ch, order=order, limit=self._items_per_page, offset=pager['offset'])
        
        domain_mng += [
            ('employee_id.parent_id.user_id', 'in', [request.env.user.id,]),
            
        ]
        over_times_manager = over_time_obj.sudo().search(domain_mng, order=order, limit=self._items_per_page, offset=pager['offset'])
        
       
        values.update({
            'over_times': over_times,
            'over_times_coach': over_times_coach,
            'over_times_manager': over_times_manager,
            'page_name': 'over_times',
            'sortings' : sortings,
            'searchbar_sortings': searchbar_sortings,
            'searchbar_inputs':searchbar_inputs,
            'sortby': sortby,
            'search_in': search_in,
            'search': search,
            'pager': pager,
            'default_url': '/my/over_time_request',
        })
        return request.render("centione_portal_hr_self_service.display_over_times", values)


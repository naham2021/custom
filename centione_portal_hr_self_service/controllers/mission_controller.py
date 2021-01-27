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
        mission = request.env['hr.mission']
        mission_count = mission.sudo().search_count([
        ('employee_id', 'in', [employee,]),
        
          ])
        values.update({
        'mission_count': mission_count,
        })
        return values
    
    @http.route(['/my/mission_request', '/my/mission_request/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_mission_request(self, page=1, sortby=None, search=None, search_in='all',**kw):
        if not request.env.user.has_group('centione_portal_hr_self_service.group_portal_mission'):
            # return request.render("odoo_timesheet_portal_user_employee.not_allowed_leave_request")
            return request.render("centione_portal_hr_self_service.not_allowed_mission_request")
        response = super(CustomerPortal, self)
        values = self._prepare_portal_layout_values()
        mission_obj = http.request.env['hr.mission']
        domain = [
            ('employee_id', 'in', [request.env.user.employee_id.id,]),
            
        ]
        # count for pager
        mission_count = http.request.env['hr.mission'].sudo().search_count(domain)

        pager = portal_pager(
            url="/my/leaves",
            total=mission_count,
            page=page,
            step=self._items_per_page
        )
        sortings = {
            'date': {'label': _('Newest'), 'order': 'state,start_date desc'},
        }
        searchbar_sortings = {
            'date': {'label': _('Exeuce Date'), 'order': 'start_date desc'},
            
             'state': {'label': _('Status'), 'order': 'state'},
        }
        searchbar_input = {
            'input': {'label': _('Exeuce Date'), 'input': 'start_date'},
            
             'state': {'label': _('Status'), 'order': 'state'},
        }
        searchbar_inputs = {
            'comment': {'input': 'comment', 'label': _('Search in Comment')},
            'state': {'input': 'state', 'label': _('Search in State')},
            'all': {'input': 'all', 'label': _('Search in All')},
        }
        domain_mng = []
        domain_ch=[]
        if search and search_in:
            search_domain = []
            if search_in in ('state', 'all'):
                search_domain = OR([search_domain, [('state', 'ilike', search),]])
            if search_in in ('comment', 'all'):
                search_domain = OR([search_domain, [('comment', 'ilike', search),]])
        
            domain += search_domain
            domain_ch += search_domain
            domain_mng += search_domain

        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']
        
        # content according to pager and archive selected
        missions = mission_obj.sudo().search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        domain_ch += [
            ('employee_id.coach_id.user_id', 'in', [request.env.user.id,]),
            
        ]
        
        missions_coach = mission_obj.sudo().search(domain_ch, order=order, limit=self._items_per_page, offset=pager['offset'])
        
        domain_mng += [
            ('employee_id.parent_id.user_id', 'in', [request.env.user.id,]),
            
        ]
        missions_manager = mission_obj.sudo().search(domain_mng, order=order, limit=self._items_per_page, offset=pager['offset'])
        print(">>>>>>>>>>>>>>>>>>>>>>.domain_mng ",domain_mng)
        print(">>>>>>>>>>>>>>>>>>>>>>.excuses_coach ",missions_manager)
       
        values.update({
            'missions': missions,
            'missions_coach':missions_coach,
            'missions_manager':missions_manager,
            'page_name': 'Missions',
            'sortings' : sortings,
            'searchbar_sortings': searchbar_sortings,
            'searchbar_inputs':searchbar_inputs,
            'sortby': sortby,
            'search_in': search_in,
            'search': search,
            'pager': pager,
            'default_url': '/my/mission_request',
        })
        return request.render("centione_portal_hr_self_service.display_missions", values)


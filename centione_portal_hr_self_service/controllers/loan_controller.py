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
        loan = request.env['hr.loan']
        loan_count = loan.sudo().search_count([
        ('employee_id', 'in', [employee,]),
        
          ])
        values.update({
        'loan_count': loan_count,
        })
        return values
    
    @http.route(['/my/loan_request', '/my/loan_request/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_loan_request(self, page=1, sortby=None, search=None, search_in='all',**kw):
        if not request.env.user.has_group('centione_portal_hr_self_service.group_portal_loan'):
            # return request.render("odoo_timesheet_portal_user_employee.not_allowed_leave_request")
            return request.render("centione_portal_hr_self_service.not_allowed_loan_request")
        response = super(CustomerPortal, self)
        values = self._prepare_portal_layout_values()
        loan_obj = http.request.env['hr.loan']
        domain = [
            ('employee_id', 'in', [request.env.user.employee_id.id,]),
            
        ]
        # count for pager
        loan_count = http.request.env['hr.loan'].sudo().search_count(domain)

        pager = portal_pager(
            url="/my/leaves",
            total=loan_count,
            page=page,
            step=self._items_per_page
        )
        sortings = {
            'date': {'label': _('Newest'), 'order': 'state,requested_date desc'},
        }
        searchbar_sortings = {
            'date': {'label': _('Request Date'), 'order': 'requested_date desc'},
            
             'state': {'label': _('Status'), 'order': 'state'},
        }
        searchbar_input = {
            'input': {'label': _('Request Date'), 'input': 'requested_date'},
            
             'state': {'label': _('Status'), 'order': 'state'},
        }
        searchbar_inputs = {
            'name': {'input': 'name', 'label': _('Search in Name')},
            'state': {'input': 'state', 'label': _('Search in State')},
            'loan_type': {'input': 'loan_type', 'label': _('Search in Loan Type')},
            'all': {'input': 'all', 'label': _('Search in All')},
        }
        
        domain_mng = []
        domain_ch=[]
        if search and search_in:
            search_domain = []
            if search_in in ('state', 'all'):
                search_domain = OR([search_domain, [('state', 'ilike', search),]])
            if search_in in ('loan_type', 'all'):
                search_domain = OR([search_domain, [('loan_type', 'ilike', search),]])
            if search_in in ('name', 'all'):
                search_domain = OR([search_domain, [('name', 'ilike', search),]])
        
            domain += search_domain
            domain_ch += search_domain
            domain_mng += search_domain

        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']
        
        # content according to pager and archive selected
        loans = loan_obj.sudo().search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        loans = loan_obj.sudo().search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        domain_ch += [
            ('employee_id.coach_id.user_id', 'in', [request.env.user.id,]),
            
        ]
        
        loans_coach = loan_obj.sudo().search(domain_ch, order=order, limit=self._items_per_page, offset=pager['offset'])
        
        domain_mng += [
            ('employee_id.parent_id.user_id', 'in', [request.env.user.id,]),
            
        ]
        loans_manager = loan_obj.sudo().search(domain_mng, order=order, limit=self._items_per_page, offset=pager['offset'])
        
        values.update({
            
            'loans': loans,
            'loans_coach':loans_coach,
            'loans_manager':loans_manager,
            'page_name': 'loans',
            'sortings' : sortings,
            'searchbar_sortings': searchbar_sortings,
            'searchbar_inputs':searchbar_inputs,
            'sortby': sortby,
            'search_in': search_in,
            'search': search,
            'pager': pager,
            'default_url': '/my/loan_request',
        })
        return request.render("centione_portal_hr_self_service.display_loans", values)


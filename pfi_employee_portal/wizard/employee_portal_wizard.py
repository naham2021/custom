# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging

LOGGER = logging.getLogger(__name__)

class EmployeePortalWizard(models.TransientModel):
    _name = 'employee.portal.wizard'


    def _default_name(self):
        return self._context.get('emp_name',False)

    def _default_email(self):
        return self._context.get('emp_email')

    name = fields.Char(string="Name",default=_default_name ,required=False, )
    email = fields.Char(string="Email",default=_default_email , required=False, )

    is_portal = fields.Boolean(string="User Portal Group",default= True,  )
    is_portal_attendance = fields.Boolean(string="Portal Attendance",default= True,  )
    is_portal_leave = fields.Boolean(string="Portal Leave",default= True,  )

    #@api.multi
    def allow_portal_access(self):
        partner = self.env['res.partner'].create({
            'name':self.name,
            'email':self.email,
        })

        context = dict(self._context)
        context.update({'employee_id': self.env.context.get('active_id')})
        context.update({'active_ids':[partner.id]})


        return {

            'name': 'Employee Portal',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'portal.wizard',
            # 'view_id': self.env.ref('pfi_employee_portal.view_employee_portal_wizard_form').id,
            # 'views': [(self.env.ref('pfi_employee_portal.view_employee_portal_wizard_form').id, 'form')],

            # 'view_id': False,
            'context': context,
            'target': 'new',


        }

        # contact_ids = set()
        # contact_partners = partner.child_ids or [partner]
        # user_changes = []
        # portal_wizard = self.env['portal.wizard'].create({})
        # for contact in contact_partners:
        #     # make sure that each contact appears at most once in the list
        #     if contact.id not in contact_ids:
        #         contact_ids.add(contact.id)
        #         in_portal = False
        #         if contact.user_ids:
        #             in_portal = portal_wizard.portal_id in contact.user_ids[0].groups_id
        #         user_changes.append((0, 0, {
        #             'partner_id': contact.id,
        #             'email': contact.email,
        #             'in_portal': in_portal,
        #         }))
        # portal_wizard.user_ids = user_changes













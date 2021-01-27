# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging

LOGGER = logging.getLogger(__name__)

class HrEmployee(models.Model):
    _inherit = 'hr.employee'



    #@api.multi
    def convert_emp_portal(self):

        portal_user_group = self.env.ref('base.group_portal')
        # portal_attendance_group = self.env.ref('odoo_portal_attendance.portal_user_employee_attendance')
        portal_leave_group = self.env.ref('odoo_leave_request_portal_employee.group_employee_leave')

        if self.user_id.id:
            portal_user_group.users = [(4, self.user_id.id, 0)]
            # portal_attendance_group.users = [(4, self.user_id.id, 0)]
            portal_leave_group.users = [(4, self.user_id.id, 0)]
            return True
        else:
            context = dict(self._context)
            context.update({'emp_name':self.name})
            context.update({'emp_email':self.work_email})

            return {

                'name': 'Employee Portal',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'view_type': 'form',
                'res_model': 'employee.portal.wizard',
                'view_id': self.env.ref('pfi_employee_portal.view_employee_portal_wizard_form').id,
                'views': [(self.env.ref('pfi_employee_portal.view_employee_portal_wizard_form').id, 'form')],

                # 'view_id': False,
                'context': context,
                'target': 'new' ,

                # 'view_id': compose_form.id,

            }






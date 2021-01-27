# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging

LOGGER = logging.getLogger(__name__)

class PortalWizard(models.TransientModel):
    _inherit = 'portal.wizard'

    #@api.multi
    def action_apply(self):
        self.ensure_one()
        self.user_ids.action_apply()
        if self.env.context.get('employee_id'):
            portal_user_group = self.env.ref('base.group_portal')
            # portal_attendance_group = self.env.ref('odoo_portal_attendance.portal_user_employee_attendance')
            portal_leave_group = self.env.ref('odoo_leave_request_portal_employee.group_employee_leave')

            for partner in self.user_ids.partner_id:
                emp = self.env['hr.employee'].browse(self.env.context.get('employee_id'))
                emp.update({'user_id':partner.user_ids[0] if partner.user_ids else False})
                portal_user_group.users = [(4, emp.user_id.id, 0)]
                # portal_attendance_group.users = [(4, emp.user_id.id, 0)]
                portal_leave_group.users = [(4, emp.user_id.id, 0)]

        return {'type': 'ir.actions.act_window_close'}


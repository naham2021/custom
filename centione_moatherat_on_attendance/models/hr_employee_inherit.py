# -*- coding: utf-8 -*-

from odoo import models, fields, api

class hr_employee(models.Model):
    _inherit = 'hr.employee'

    def get_overtime_custom_val(self,payslip):
        late_records = self.env['moatherat.attendance'].search([
            ('employee_id', '=', self.id),
            ('moather_type', '=', 'overtime'),
            ('from_date', '>=', payslip.date_from),
            ('to_date', '<=', payslip.date_to),

        ])
        result = 0
        for rec in late_records:
            result += rec.value
        return result

    def get_early_leave_custom_val(self,payslip):
        early_leave_records = self.env['moatherat.attendance'].search([
            ('employee_id', '=', self.id),
            ('moather_type', '=', 'early_leave'),
            ('from_date', '>=', payslip.date_from),
            ('to_date', '<=', payslip.date_to),

        ])
        result = 0
        for rec in early_leave_records:
            result += rec.value
        return result

    def get_absent_custom_val(self,payslip):
        absent_records = self.env['moatherat.attendance'].search([
            ('employee_id', '=', self.id),
            ('moather_type', '=', 'absent'),
            ('from_date', '>=', payslip.date_from),
            ('to_date', '<=', payslip.date_to),

        ])
        result = 0
        for rec in absent_records:
            result += rec.value
        return result

    def get_late_custom_val(self,payslip):
        late_records=self.env['moatherat.attendance'].search([
            ('employee_id','=',self.id),
            ('moather_type','=','late'),
            ('from_date','>=',payslip.date_from),
            ('to_date','<=',payslip.date_to),

        ])
        result=0
        for rec in late_records:
            result+=rec.value
        return result

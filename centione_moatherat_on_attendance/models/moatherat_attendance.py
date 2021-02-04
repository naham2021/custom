# -*- coding: utf-8 -*-

from odoo import models, fields, api


class moatherat_attendance(models.Model):
    _name = 'moatherat.attendance'

    moather_type = fields.Selection([
        ('absent', 'غياب بدون اذن'),
        ('early_leave', 'انصراف مبكر'),
        ('late', 'تأخير'),
        ('overtime', 'اضافي'),
    ], string="نوع المؤثر")
    overtime_type = fields.Selection([('اضافي', 'اضافي'), ('نبتشية', 'اضافي نبتشية')], string="نوع الاضافي")

    from_date = fields.Date('من')
    to_date = fields.Date('الي')
    employee_id = fields.Many2one('hr.employee', string='الموظف')
    job_id = fields.Many2one(related='employee_id.job_id', string='الوظيفة', store=True)

    num_of_times = fields.Integer('عدد المرات')
    num_of_hours = fields.Integer('عدد الساعات')

    def get_ovetime_allow_value(self, num_of_hours, employee_id, overtime_type):
        overtime_allow = self.env['custom.deductions'].search([
            ('overtime_type', '=', overtime_type),
            ('moather_type', '=', 'overtime')], limit=1)
        if overtime_allow:
            return overtime_allow.hour_value * num_of_hours

    def get_absent_ded_value(self,num_of_times, employee_id):
        late_deduc = self.env['custom.deductions'].search([('late_time', '<=', num_of_times),
                                                                  ('moather_type', '=', 'absent')])
        deduc_val = 0
        for rec in late_deduc:
            deduc_val += rec.deduction_value
        return (deduc_val / 100) * (employee_id.contract_id.wage / 30)

    def get_early_leave_ded_value(self,num_of_times, employee_id):
        early_leave_deduc = self.env['custom.deductions'].search([('late_time', '<=', num_of_times),
                                                           ('moather_type', '=', 'early_leave')])
        deduc_val = 0
        for rec in early_leave_deduc:
            deduc_val += rec.deduction_value
        return (deduc_val / 100) * (employee_id.contract_id.wage / 30)

    def get_late_ded_value(self, num_of_times, employee_id):
        late_deduc = self.env['custom.deductions'].search([('late_time', '<=', num_of_times),
                                                           ('moather_type', '=', 'late')])
        deduc_val = 0
        for rec in late_deduc:
            deduc_val += rec.deduction_value
        return (deduc_val / 100) * (employee_id.contract_id.wage / 30)


    @api.onchange('employee_id', 'moather_type','overtime_type','num_of_times', 'num_of_hours')
    @api.depends('moather_type', 'employee_id', 'num_of_times', 'num_of_hours','overtime_type')
    def _compute_value(self):
        for rec in self:
            if rec.moather_type == 'late' and rec.num_of_times > 0:
                rec.value = rec.get_late_ded_value(rec.num_of_times, rec.employee_id)
            elif rec.moather_type == 'overtime' and rec.num_of_hours > 0:
                rec.value = rec.get_ovetime_allow_value(rec.num_of_hours, rec.employee_id, rec.overtime_type)
            elif rec.moather_type == 'early_leave' and rec.num_of_times > 0:
                rec.value = rec.get_early_leave_ded_value(rec.num_of_times, rec.employee_id)
            elif rec.moather_type == 'absent' and rec.num_of_times > 0:
                rec.value = rec.get_absent_ded_value(rec.num_of_times, rec.employee_id)

    value = fields.Float(string='القيمة', compute=_compute_value, store=True, )

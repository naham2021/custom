# -*- coding: utf-8 -*-

from odoo import models, fields, api

class custom_deductions(models.Model):
    _name = 'custom.deductions'

    late_time=fields.Integer('المرة')
    deduction_value=fields.Float('نسبة الخصم')
    overtime_type = fields.Selection([('اضافي', 'اضافي'), ('نبتشية', 'اضافي نبتشية')], string="النوع")
    hour_value=fields.Float('قيمة الساعة')
    moather_type = fields.Selection([
        ('absent', 'غياب بدون اذن'),
        ('early_leave', 'انصراف مبكر'),
        ('late', 'تأخير'),
        ('overtime', 'اضافي'),
    ], string="نوع المؤثر")

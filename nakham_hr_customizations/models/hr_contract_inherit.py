# -*- coding: utf-8 -*-

from odoo import models, fields, api

class hr_contract_inherit(models.Model):
    _inherit = 'hr.contract'

    movements_val=fields.Float('انتقال')
    basic_salary=fields.Float('راتب اساسي')
    housing_val=fields.Float('سكن')
    end_of_service_val=fields.Float('نهاية خدمة')
    air_tickets=fields.Float('تذاكر طيران')
    vacation_salary=fields.Float('راتب اجازة')



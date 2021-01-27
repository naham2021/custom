from odoo import models, fields, api, _
from odoo.exceptions import UserError

from datetime import datetime
import calendar


class HrExcuse(models.Model):
    _name = 'hr.excuse'
    _inherit = 'hr.self.service'

    start_date = fields.Datetime()
    end_date = fields.Datetime()
    period = fields.Float(compute='_compute_period', store=True)

    @api.constrains('period')
    def _check_period(self):
        max_period = self.employee_id.max_excuse_period
        if self.period > max_period:
            raise UserError(_('Period exceeds employee\'s allowed period.'))
        month = self.start_date.month
        year = self.start_date.year
        month_start = datetime(day=1, month=month, year=year, hour=0, minute=0, second=0)
        month_end = datetime(day=calendar.monthrange(year, month)[1], month=month, year=year, hour=23, minute=59, second=59)
        max_month_request = self.employee_id.number_excuse_per_month
        excuses_this_month = self.env['hr.excuse'].search([('employee_id', '=', self.employee_id.id),
                                                           ('start_date', '>=', month_start),
                                                           ('end_date', '<=', month_end),
                                                           ('state', '=', 'validate')])
        if len(excuses_this_month) >= max_month_request:
            raise UserError(_('Period exceeds employee\'s allowed requests per month.'))


    @api.depends('start_date', 'end_date')
    def _compute_period(self):
        if self.end_date and self.start_date:
            self.period = (self.end_date - self.start_date).total_seconds() / 3600.0

    def validate(self):
        super(HrExcuse, self).validate()
        self.env['resource.calendar.leaves'].create({
            'name': 'HR Excuse: %s' % (self.comment if self.comment else ''),
            'resource_id': self.employee_id.resource_id.id,
            'calendar_id': self.employee_id.resource_calendar_id.id,
            'date_from': self.start_date,
            'date_to': self.end_date
        })
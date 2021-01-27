from odoo import models, fields, api, _


class HrMission(models.Model):
    _name = 'hr.mission'
    _inherit = 'hr.self.service'

    start_date = fields.Datetime()
    end_date = fields.Datetime()
    period = fields.Float(compute='_compute_period')

    @api.depends('start_date', 'end_date')
    def _compute_period(self):
        for rec in self:
            rec.period = 0
            if rec.end_date and rec.start_date:
                rec.period = (rec.end_date - rec.start_date).total_seconds() / 3600.0

    def validate(self):
        super(HrMission, self).validate()
        self.env['resource.calendar.leaves'].create({
            'name': 'HR Mission: %s' % (self.comment if self.comment else ''),
            'resource_id': self.employee_id.resource_id.id,
            'calendar_id': self.employee_id.resource_calendar_id.id,
            'date_from': self.start_date,
            'date_to': self.end_date
        })

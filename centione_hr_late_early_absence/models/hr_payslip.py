from odoo import models, fields, api, _
from datetime import timedelta

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    def compute_sheet(self):
        for rec in self:
            leaves = self.env['resource.calendar.leaves'].search([('holiday_id.employee_id.id', '=', rec.employee_id.id)])
            for it in leaves:
                it.reset_consume_hours()
        res = super(HrPayslip, self).compute_sheet()
        return res

    @api.model
    def get_worked_day_lines(self, contracts, date_from, date_to):
        res = super(HrPayslip, self).get_worked_day_lines(contracts, date_from, date_to)
        absence_records = self.env['hr.absence'].search([
            ('employee_id', '=', self.employee_id.id),
            ('date', '>=', date_from),
            ('date', '<=', date_to)
        ])
        total_absence_days = len(absence_records)
        total_absence_hours = total_absence_days * self.employee_id.resource_calendar_id.hours_per_day if self.employee_id.resource_calendar_id else 0
        if total_absence_days and total_absence_hours:
            absence = {
                'name': 'Absence',
                'sequence': 3,
                'code': 'ABSENCE',
                'number_of_days': -1 * total_absence_days,
                'number_of_hours': -1 * total_absence_hours,
                'contract_id': self.contract_id.id,
            }
            res.append(absence)
        return res

    def compute_absence_penalty(self, payslip):
        payslip = payslip.dict
        resource_calendar = payslip.employee_id.resource_calendar_id
        wage = payslip.contract_id.wage
        wage_per_day = wage / 30.0
        total_absence_days = 0
        absence_penalty_rate = []
        for it in payslip.worked_days_line_ids:
            if it.code == 'ABSENCE':
                total_absence_days = abs(it.number_of_days)
                break

        if resource_calendar.absence_penalty_type == 'fixed':
            absence_penalty_rate = [resource_calendar.absence_penalty_fixed_rate]
        elif resource_calendar.absence_penalty_type == 'cumulative':
            absence_penalty_rate = [it.penalty_rate for it in resource_calendar.absence_penalty_line_ids]

        result = 0
        while total_absence_days > 0:
            if len(absence_penalty_rate) > 1:
                rate = absence_penalty_rate.pop(0)
                result += rate * wage_per_day
                total_absence_days -= 1
            elif len(absence_penalty_rate) == 1:
                result += absence_penalty_rate[0] * total_absence_days * wage_per_day
                total_absence_days = 0
            else:
                result += total_absence_days * wage_per_day
                total_absence_days = 0

        return -1 * result

    def _get_polices(self, raw_policy):
        res = []
        for it in raw_policy:
            res.append(
                ((it.first_operand, it.second_operand if it.second_operand else float('inf')),
                [x.penalty_value for x in it.late_early_penalty_line_ids]))
        return res

    def _get_policy_idx(self, time, policy):
        for idx, lp in enumerate(policy):
            if lp[0][0] <= time <= lp[0][1]:
                return idx
        return -1

    def compute_late_arrive_penalty(self, payslip):
        payslip = payslip.dict
        working_schedule = payslip.employee_id.resource_calendar_id
        wage = payslip.contract_id.wage
        wage_per_day = wage / 30.0
        wage_per_hour = wage_per_day / working_schedule.hours_per_day

        date_from = fields.Datetime.to_datetime(payslip.date_from)
        date_to = fields.Datetime.to_datetime(payslip.date_to) + timedelta(hours=23, minutes=59, seconds=59)
        late_days = self.env['hr.attendance'].search([('employee_id', '=', payslip.employee_id.id),
                                                      ('check_in', '>=', date_from),
                                                      ('check_in', '<=', date_to),
                                                      ('late_attendance_hours', '>', 0)])
        late_days = [DummyAttendance(it) for it in late_days]
        leaves = self.env['resource.calendar.leaves'].search([('holiday_id.employee_id.id', '=', payslip.employee_id.id)])
        for idx in range(0, len(late_days)):
            for leave in leaves:
                if late_days and leave.date_from.date() <= late_days[idx].check_in.date() <= leave.date_to.date():
                    if leave.consume_hours >= late_days[idx].late_attendance_hours:
                        leave.consume_hours -= late_days[idx].late_attendance_hours
                        late_days[idx].late_attendance_hours = 0
                    elif leave.consume_hours:
                        late_days[idx].late_attendance_hours -= leave.consume_hours
                        leave.consume_hours = 0

        late_days = list(filter(lambda a: a.late_attendance_hours != 0, late_days))
        total_late_hours = sum([it.late_attendance_hours for it in late_days])
        total_penalty = 0
        if working_schedule.late_arrive_penalty_type == 'fixed':
            total_penalty = total_late_hours * working_schedule.late_arrive_penalty_fixed_rate * wage_per_hour
        elif working_schedule.late_arrive_penalty_type == 'cumulative':
            late_policy = self._get_polices(working_schedule.late_arrive_penalty_line_ids)
            total_penalty_time = 0
            for it in late_days:
                idx = self._get_policy_idx(it.late_attendance_hours, late_policy)
                total_penalty_time += late_policy[idx][1][0] if late_policy and late_policy[idx][1] else it.late_attendance_hours
                if late_policy and len(late_policy[idx][1]) > 1:
                    late_policy[idx][1][0].pop(0)

            total_penalty = total_penalty_time * wage_per_hour

        return -1 * total_penalty

    def compute_early_leave_penalty(self, payslip):
        payslip = payslip.dict
        working_schedule = payslip.employee_id.resource_calendar_id
        wage = payslip.contract_id.wage
        wage_per_day = wage / 30.0
        wage_per_hour = wage_per_day / working_schedule.hours_per_day

        date_from = fields.Datetime.to_datetime(payslip.date_from)
        date_to = fields.Datetime.to_datetime(payslip.date_to) + timedelta(hours=23, minutes=59, seconds=59)
        early_days = self.env['hr.attendance'].search([('employee_id', '=', payslip.employee_id.id),
                                                      ('check_in', '>=', date_from),
                                                      ('check_in', '<=', date_to),
                                                      ('early_leave_hours', '>', 0)])
        early_days = [DummyAttendance(it) for it in early_days]
        leaves = self.env['resource.calendar.leaves'].search([('holiday_id.employee_id.id', '=', payslip.employee_id.id)])
        for idx in range(0, len(early_days)):
            for leave in leaves:
                if early_days and leave.date_from.date() <= early_days[idx].check_in.date() <= leave.date_to.date():
                    if leave.consume_hours >= early_days[idx].early_leave_hours:
                        leave.consume_hours -= early_days[idx].early_leave_hours
                        early_days[idx].early_leave_hours = 0
                    elif leave.consume_hours:
                        early_days[idx].early_leave_hours -= leave.consume_hours
                        leave.consume_hours = 0

        early_days = list(filter(lambda a: a.early_leave_hours != 0, early_days))
        total_early_hours = sum([it.early_leave_hours for it in early_days])
        total_penalty = 0
        if working_schedule.early_leave_penalty_type == 'fixed':
            total_penalty = total_early_hours * working_schedule.early_leave_penalty_fixed_rate * wage_per_hour
        elif working_schedule.early_leave_penalty_type == 'cumulative':
            early_policy = self._get_polices(working_schedule.early_leave_penalty_line_ids)
            total_penalty_time = 0
            for it in early_days:
                idx = self._get_policy_idx(it.early_leave_hours, early_policy)
                total_penalty_time += early_policy[idx][1][0] if early_policy and early_policy[idx][1] else it.early_leave_hours
                if early_policy and len(early_policy[idx][1]) > 1:
                    early_policy[idx][1][0].pop(0)

            total_penalty = total_penalty_time * wage_per_hour

        return -1 * total_penalty


class DummyAttendance:
    def __init__(self, attendance):
        self.check_in = attendance.check_in
        self.check_out = attendance.check_out
        self.late_attendance_hours = attendance.late_attendance_hours
        self.early_leave_hours = attendance.early_leave_hours

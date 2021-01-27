from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AbstractModel(models.AbstractModel):
    _inherit = 'hr.self.service'

    def confirm(self):
        if self.env.user.id == self.employee_id.user_id.id:
            self.state = 'confirm'
        else:
            raise UserError('Only Employee Requester can confirm ')


    def approve(self):
        if self.env.user.id == self.employee_id.coach_id.user_id.id :
            # self.update({'is_coach_id':True})
            self.state = 'approve'
        else:
            # self.update({'is_coach_id':False})
            raise UserError('Only Employee Coach  can Approve this Request!! ')
        

    def validate(self):
        if self.env.user.id == self.employee_id.parent_id.user_id.id :
            # self.update({'is_coach_id':True})
            self.state = 'validate'
        else:
            # self.update({'is_coach_id':False})
            raise UserError('Only Employee Manager can Approve this Request!! ')
        

    def refuse(self):
        if self.env.user.id in [self.employee_id.parent_id.user_id.id,self.employee_id.coach_id.user_id.id]  :
            # self.update({'is_coach_id':True})
            self.state = 'refuse'
        else:
            # self.update({'is_coach_id':False})
            raise UserError('Only Employee Manager or Coach can Refuse this Request!! ')
        

    def draft(self):
        if self.env.user.id in [self.employee_id.parent_id.user_id.id,self.employee_id.coach_id.user_id.id]  :
            # self.update({'is_coach_id':True})
            self.state = 'draft'
        else:
            # self.update({'is_coach_id':False})
            raise UserError('Only Employee Manager or Coach can Draft this Request!! ')

    def _default_employee(self):
        return self.env.context.get('default_employee_id') or self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)

    employee_id = fields.Many2one('hr.employee',default=_default_employee)
    # state = fields.Selection(selection_add=[('confirm', 'Confirm')])
    state = fields.Selection([('draft', 'Draft'),('confirm', 'Confirm'), ('approve', 'Approved'), ('validate', 'Validated'), ('refuse', 'Refused')],
                             default='draft')
    # parent_id = fields.Many2one('res.users', 'Manager', related="employee_id.parent_id.user_id")
    # coach_id = fields.Many2one('res.users', 'Coach',related="employee_id.coach_id.user_id")
    # current_user = fields.Many2one('res.users', compute='_get_current_user')
    # is_coach_id = fields.Boolean(compute='_check_managers_user')
    # is_manager_id = fields.Boolean(compute='_check_managers_user')
    
    # @api.depends('employee_id')
    # def _check_managers_user(self):
    #     if self.env.user.id == self.employee_id.coach_id.user_id.id and self.state == 'confirm':
    #         self.update({'is_coach_id':True})
    #     else:
    #         self.update({'is_coach_id':False})
        
    #     if self.env.user.id == self.employee_id.parent_id.user_id.id and self.state == 'confirm':
    #         self.update({'is_manager_id':True})
    #     else:
    #         self.update({'is_manager_id':False})
    # @api.depends()
    # def _get_current_user(self):
    #     for rec in self:
    #         rec.current_user = self.env.user
    #     # i think this work too so you don't have to loop
    #     self.update({'current_user' : self.env.user.id})

    # employee_id = fields.Many2one(
    #     'hr.employee', string='Employee', index=True, readonly=True, ondelete="restrict",
    #     states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]}, default=_default_employee, tracking=True)
    


class HrLoan(models.Model):
    _inherit = 'hr.loan'

    def _default_employee(self):
        return self.env.context.get('default_employee_id') or self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True,default=_default_employee)

class HrOvertime(models.Model):
    _inherit = 'over.time'

    def _default_employee(self):
        return self.env.context.get('default_employee_id') or self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)

    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee", required=False,default=_default_employee )
    
    # state = fields.Selection(string="", selection=[('draft', 'Draft'), ('approved', 'Approved'), ('done', 'Done')],
    #                          default='draft')

    state = fields.Selection([('draft', 'Draft'),('confirm', 'Confirm'), ('approve', 'Approved'), ('validate', 'Validated'), ('refuse', 'Refused')],
                             default='draft')

    def action_done(self):
        for rec in self:
            rec.write({'state': 'done'})

    def action_approve(self):
        for rec in self:
            rec.write({'state': 'approved'})

    def confirm(self):
        if self.env.user.id == self.employee_id.user_id.id:
            self.state = 'confirm'
        else:
            raise UserError('Only Employee Requester can confirm ')


    def approve(self):
        if self.env.user.id == self.employee_id.coach_id.user_id.id :
            # self.update({'is_coach_id':True})
            self.state = 'approve'
        else:
            # self.update({'is_coach_id':False})
            raise UserError('Only Employee Coach  can Approve this Request!! ')
        

    def validate(self):
        if self.env.user.id == self.employee_id.parent_id.user_id.id :
            # self.update({'is_coach_id':True})
            self.state = 'validate'
        else:
            # self.update({'is_coach_id':False})
            raise UserError('Only Employee Manager can Approve this Request!! ')
        

    def refuse(self):
        if self.env.user.id in [self.employee_id.parent_id.user_id.id,self.employee_id.coach_id.user_id.id]  :
            # self.update({'is_coach_id':True})
            self.state = 'refuse'
        else:
            # self.update({'is_coach_id':False})
            raise UserError('Only Employee Manager or Coach can Refuse this Request!! ')
        

    def draft(self):
        if self.env.user.id in [self.employee_id.parent_id.user_id.id,self.employee_id.coach_id.user_id.id]  :
            # self.update({'is_coach_id':True})
            self.state = 'draft'
        else:
            # self.update({'is_coach_id':False})
            raise UserError('Only Employee Manager or Coach can Draft this Request!! ')






class HrLoan(models.Model):
    _inherit = 'hr.loan'

    # state = fields.Selection(
    #     [('draft', 'Draft'), ('cancel', 'Cancelled'),
    #      ('approved', 'Approved'), ('sent', 'Sent'), ('closed', 'Closed')],
    #     default='draft',
    #     readonly=True,
    #     copy=False,
    #     track_visibility='onchange')
    
    state = fields.Selection([('draft', 'Draft'),('confirm', 'Confirm'), ('approved', 'Approved'),
     ('validate', 'Validated'), ('refuse', 'Refused'),('sent', 'Sent'),('closed','Closed')],
                             default='draft',copy=False,track_visibility='onchange')


    def confirm(self):
        if self.env.user.id == self.employee_id.user_id.id:
            if self.loan_line:
                requested_amount = self.requested_amount

                total_amount = sum((one_line.amount - one_line.paid_amount) for one_line in self.loan_line)
                if total_amount != requested_amount:
                    raise UserError(_('Error ! Total Amount In lines Must Be Equal The Requested Amount.'))
                self.state = 'confirm'
            else:
                raise UserError(_('Error ! You Cannot Approved Without Lines .'))
            return True

        
            
        else:
            raise UserError('Only Employee Requester can confirm ')


    def approve(self):
        if self.env.user.id == self.employee_id.coach_id.user_id.id :
            # self.update({'is_coach_id':True})
            self.state = 'approved'
        else:
            # self.update({'is_coach_id':False})
            raise UserError('Only Employee Coach  can Approve this Request!! ')
        

    def validate(self):
        if self.env.user.id == self.employee_id.parent_id.user_id.id :
            # self.update({'is_coach_id':True})
            # self.action_approved()
            self.state = 'validate'
        else:
            # self.update({'is_coach_id':False})
            raise UserError('Only Employee Manager can Approve this Request!! ')
        

    def refuse(self):
        if self.env.user.id in [self.employee_id.parent_id.user_id.id,self.employee_id.coach_id.user_id.id]  :
            # self.update({'is_coach_id':True})
            self.action_cancel()
            self.state = 'refuse'
        else:
            # self.update({'is_coach_id':False})
            raise UserError('Only Employee Manager or Coach can Refuse this Request!! ')
        

    def draft(self):
        if self.env.user.id in [self.employee_id.parent_id.user_id.id,self.employee_id.coach_id.user_id.id]  :
            # self.update({'is_coach_id':True})
            self.state = 'draft'
        else:
            # self.update({'is_coach_id':False})
            raise UserError('Only Employee Manager or Coach can Draft this Request!! ')


class HrLeave(models.Model):
    _inherit = 'hr.leave'



    state = fields.Selection([
        ('draft', 'Draft'),
        ('cancel', 'Cancelled'),
        ('confirm', 'Confirmed'),
        ('refuse', 'Refused'),
        ('validate1', 'Validated'),
        ('validate', 'Approved')
        ], string='Status', readonly=True, tracking=True, copy=False, default='draft',
        help="The status is set to 'To Submit', when a time off request is created." +
        "\nThe status is 'To Approve', when time off request is confirmed by user." +
        "\nThe status is 'Refused', when time off request is refused by manager." +
        "\nThe status is 'Approved', when time off request is approved by manager.")
    


    @api.model
    def create(self, values):
        """ Override to avoid automatic logging of creation """
        holiday = super(HrLeave, self).create(values)
        holiday.state = 'draft'
        return holiday


    @api.onchange('holiday_status_id')
    def _onchange_holiday_status_id(self):
        self.request_unit_half = False
        self.request_unit_hours = False
        self.request_unit_custom = False
        self.state = 'draft' #if self.validation_type != 'no_validation' else 'draft'
    
    
    def action_draft(self):
        
        if self.env.user.id in [self.employee_id.parent_id.user_id.id,self.employee_id.coach_id.user_id.id]  :
            res = super(HrLeave,self).action_draft()
            return res
        else:
            # self.update({'is_coach_id':False})
            raise UserError('Only Employee Manager or Coach can Draft this Request!! ')
    
    def action_confirm(self):
        if self.env.user.id == self.employee_id.user_id.id:
            res = super(HrLeave,self).action_confirm()
            return res
        else:
            raise UserError('Only Employee Requester can confirm ')
        

    def action_approve(self):
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>1")
        if self.env.user.id == self.employee_id.coach_id.user_id.id :
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>2")
            if any(holiday.state != 'confirm' for holiday in self):
                raise UserError(_('Time off request must be confirmed ("To Approve") in order to approve it.'))
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>3")
            current_employee = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>4")
            self.filtered(lambda hol: hol.validation_type == 'both').write({'state': 'validate1', 'first_approver_id': current_employee.id})
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>5")

            # Post a second message, more verbose than the tracking message
            for holiday in self.sudo().filtered(lambda holiday: holiday.employee_id.user_id):
                print(">>>>>>>>>>>>>>>>>>>>>>>>>>>6")
                holiday.sudo().message_post(
                    body=_('Your %s planned on %s has been accepted' % (holiday.holiday_status_id.display_name, holiday.date_from)),
                    partner_ids=holiday.employee_id.user_id.partner_id.ids)
                print(">>>>>>>>>>>>>>>>>>>>>>>>>>>7")
            # self.filtered(lambda hol: not hol.validation_type == 'both').action_validate()
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>8")
            if not self.env.context.get('leave_fast_create'):
                print(">>>>>>>>>>>>>>>>>>>>>>>>>>>9")
                self.sudo().activity_update()
                print(">>>>>>>>>>>>>>>>>>>>>>>>>>>10")
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>11")
            self.state  ='validate1'
            return True
        else:
            raise UserError('Only Employee Coach  can Approve this Request!! ')

    def action_validate(self):
        if self.env.user.id == self.employee_id.parent_id.user_id.id :
            res = super(HrLeave,self.sudo()).action_validate()
            return res
        else:
            # self.update({'is_coach_id':False})
            raise UserError('Only Employee Manager can Approve this Request!! ')

    def action_refuse(self):
        if self.env.user.id in [self.employee_id.parent_id.user_id.id,self.employee_id.coach_id.user_id.id]  :
            res = super(HrLeave,self).action_refuse()
            return res
        else:
            # self.update({'is_coach_id':False})
            raise UserError('Only Employee Manager can Approve this Request!! ')

    
    

    def _check_double_validation_rules(self, employees, state):
        if self.user_has_groups('hr_holidays.group_hr_holidays_manager'):
            return

        is_leave_user = self.user_has_groups('hr_holidays.group_hr_holidays_user')
        if state == 'validate1':
            employees = employees.filtered(lambda employee: employee.leave_manager_id != self.env.user)
            if employees and not is_leave_user:
                raise AccessError(_('You cannot first approve a leave for %s, because you are not his leave manager' % (employees[0].name,)))
        # elif state == 'validate' and not is_leave_user:
        #     # Is probably handled via ir.rule
        #     raise AccessError(_('You don\'t have the rights to apply second approval on a leave request'))
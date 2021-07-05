import time
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountAgedTrialBalance(models.TransientModel):
    _name = 'account.aged.trial.balance.excel'
    _inherit = 'account.common.partner.report'
    _description = 'Account Aged Trial balance Report Excel'

    period_length = fields.Integer(string='Period Length (days)', required=True, default=30)
    journal_ids = fields.Many2many('account.journal', string='Journals', required=True)
    date_from = fields.Date(default=lambda *a: time.strftime('%Y-%m-%d'))
    partner_tags = fields.Many2many('res.partner.category')


    @api.onchange('partner_tags')
    def _default_partner_tags(self):
        cust = self.env['res.partner'].search([('category_id','in',self.partner_tags.ids)])
        if self.partner_tags:
            self.partner_ids = cust.ids
        else:
            print("nnnnnnnnnnn")
            self.partner_ids =[(5,0,0)]
        # {self.partner_ids: [(4, cust.ids)]}
        # return cust


    partner_ids = fields.Many2many('res.partner')

    tags_flag = fields.Boolean('Partner Tags Flag')



    def _print_report(self, data):
        res = {}
        data = self.pre_print_report(data)
        data['form'].update(self.read(['period_length'])[0])
        period_length = data['form']['period_length']
        if period_length<=0:
            raise UserError(_('You must set a period length greater than 0.'))
        if not data['form']['date_from']:
            raise UserError(_('You must set a start date.'))

        start = data['form']['date_from']

        for i in range(5)[::-1]:
            stop = start - relativedelta(days=period_length - 1)
            res[str(i)] = {
                'name': (i != 0 and (str((5-(i+1)) * period_length) + '-' + str((5-i) * period_length)) or ('+'+str(4 * period_length))),
                'stop': start.strftime('%Y-%m-%d'),
                'start': (i != 0 and stop.strftime('%Y-%m-%d') or False),
            }
            start = stop - relativedelta(days=1)
        data['form'].update(res)
        data['form'].update(self.read(['partner_ids'])[0])
        print(self.read(['partner_ids'])[0])
        # print(type(data['form']['partner_ids']))
        return self.env.ref('naham_aged_partner_excel.action_report_aged_partner_balance_excel').sudo().report_action(self, data=data)

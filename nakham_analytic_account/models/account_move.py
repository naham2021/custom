from odoo import models, fields, api,_,exceptions

class account_invoice(models.Model):
    _inherit = 'account.move.line'

    @api.model
    def _get_default_analytic_account(self):
        print('_get_default_analytic_account')
        user = self.env['res.users'].search([('id','=',self.env.uid)], limit=1)
        analytic = self.env['account.analytic.account'].search([('id','=',user.analytic_ids.ids)], limit=1)
        print('self.move_id.type ',self.move_id.type)
        if self.move_id.type != False:
            if self.move_id.type in ['out_invoice', 'out_refund', 'in_invoice', 'in_refund', 'out_receipt', 'in_receipt']:
                return analytic
            else:
                return False
        else:
            return False

    analytic_account_id = fields.Many2one('account.analytic.account',
                                          string='Analytic Account',
                                          index=True,
                                          default=_get_default_analytic_account)

    @api.onchange('analytic_account_id')
    def onchange_method_analytic_account_id(self):
        print("user.analytic_ids.ids")
        user = self.env['res.users'].search([('id','=',self.env.uid)], limit=1)
        analytic = self.env['account.analytic.account'].search([('id','in',user.analytic_ids.ids)], limit=1)

        return {
            'domain': { 'analytic_account_id': [('id', 'in', user.analytic_ids.ids)]}
        }

from odoo import models, fields, api,_,exceptions

class sale_order(models.Model):
    _inherit = 'sale.order'

    @api.model
    def _get_default_analytic_account(self):
        print('_get_default_analytic_account')
        user = self.env['res.users'].search([('id','=',self.env.uid)], limit=1)
        analytic = self.env['account.analytic.account'].search([('id','=',user.analytic_ids.ids)], limit=1)
        print("analytic :: %s",analytic)
        return analytic

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

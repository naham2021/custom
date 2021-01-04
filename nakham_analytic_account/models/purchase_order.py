from odoo import models, fields, api,_,exceptions
from odoo.addons.purchase.models.purchase import PurchaseOrder as Purchase

class purchase_order(models.Model):
    _inherit = 'purchase.order'

    @api.model
    def _default_picking_type(self):
        print('_get_default_analytic_account--->')
        user = self.env['res.users'].search([('id', '=', self.env.uid)], limit=1)
        warehouse = self.env['stock.warehouse'].search([('user_ids', '=', user.id)],limit=1)
        print("warehouse :: %s", warehouse)
        return warehouse.in_type_id.id
        # return self._get_picking_type(self.env.context.get('company_id') or self.env.company.id)


    picking_type_id = fields.Many2one('stock.picking.type', 'Deliver To', states=Purchase.READONLY_STATES, required=True, default=_default_picking_type, domain="['|', ('warehouse_id', '=', False), ('warehouse_id.company_id', '=', company_id)]",
        help="This will determine operation type of incoming shipment" ,readonly=False)

    @api.onchange('picking_type_id')
    def onchange_method_picking_type_id(self):
        user = self.env['res.users'].search([('id', '=', self.env.uid)], limit=1)
        warehouse = self.env['stock.warehouse'].search([('user_ids', '=', user.id)])
        ids = []
        for w in warehouse:
            ids.append(w.in_type_id.id)
        return {
            'domain': { 'picking_type_id': [('id', 'in', ids)]}
        }
class purchase_order_line(models.Model):
    _inherit = 'purchase.order.line'

    @api.model
    def _get_default_analytic_account(self):
        print('_get_default_analytic_account')
        user = self.env['res.users'].search([('id','=',self.env.uid)], limit=1)
        analytic = self.env['account.analytic.account'].search([('id','=',user.analytic_ids.ids)], limit=1)
        print("analytic :: %s",analytic)
        return analytic

    def _default_analytic_line_domain(self):
        print('_get_default_analytic_account')
        user = self.env['res.users'].search([('id','=',self.env.uid)], limit=1)
        analytic = self.env['account.analytic.account'].search([('id','=',user.analytic_ids.ids)], limit=1)
        print("auser.analytic_ids.idsc3333 :: %s",user.analytic_ids.ids)
        return [('id', 'in', user.analytic_ids.ids)]


    account_analytic_id = fields.Many2one('account.analytic.account', string='Analytic Account',
                                          default=_get_default_analytic_account, domain=lambda self: self._default_analytic_line_domain())
    @api.model
    @api.onchange('account_analytic_id')
    def onchange_method_account_analytic_id(self):
        user = self.env['res.users'].search([('id', '=', self.env.uid)], limit=1)
        analytic = self.env['account.analytic.account'].search([('id', '=', user.analytic_ids.ids)])
        print('analytic 5555555::%s ',analytic.ids)
        return {
                    'domain': { 'account_analytic_id': [('id', 'in', analytic.ids)]}
                }
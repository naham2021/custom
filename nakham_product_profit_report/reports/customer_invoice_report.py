from odoo import fields, models, api


class AccountMoveLineCalPer(models.Model):
    _inherit = 'account.move.line'

    def cal_percentage(self):
        if self.price_unit:
            return (self.price_unit - self.purchase_price) / self.price_unit * 100
        return 0.0


class CustomerInvoicesRepoert(models.AbstractModel):
    _name = 'report.nakham_product_profit_report.customer_invoices_tmpl'

    @api.model
    def _get_report_values(self, docids, data=None):
        # get data
        # print(data['form']['product_ids'])
        # print(data['form']['date_from'])
        # print(data['form']['date_to'])
        # print(data['form']['partner_id'])
        # print(data['form']['salesman_id'])

        domain = [
            ('move_id.type', 'in', ['out_invoice', 'out_refund']), ]
        if data['form']['product_ids']:
            domain.append(('product_id.id', 'in', data['form']['product_ids']))
        if data['form']['date_from']:
            domain.append(('move_id.invoice_date', '>=', data['form']['date_from']))
        if data['form']['date_to']:
            domain.append(('move_id.invoice_date', '<=', data['form']['date_to']))
        if data['form']['partner_id']:
            domain.append(('move_id.partner_id.id', '=', data['form']['partner_id'][0]))
        if data['form']['salesman_id']:
            domain.append(('move_id.invoice_user_id.id', '=', data['form']['salesman_id'][0]))

        invoices = self.env['account.move.line'].search(domain, order='product_id')
        total_price_unit = sum(invoices.mapped('price_unit'))
        total_cost = sum(invoices.mapped('purchase_price'))
        # print('type of invoices', type(invoices))
        # print(total_price_unit)
        # print(total_cost)

        # print('my invoices', invoices)
        return {
            'doc_model': 'account.move',
            'data': data,
            'invoices': invoices,
            'total_price_unit': total_price_unit,
            'total_cost': total_cost
        }

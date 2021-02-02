from odoo import fields, models, api


class CustomerInvoicesRepoert(models.AbstractModel):
    _name = 'report.nakham_product_profit_report.customer_invoices_tmpl'

    @api.model
    def _get_report_values(self, docids, data=None):
        # get data
        print(data['form']['product_ids'])
        print(data['form']['date_from'])
        print(data['form']['date_to'])
        print(data['form']['partner_id'][0])
        print(data['form']['salesman_id'][0])
        domain = [
            ('move_id.type', 'in', ['out_invoice', 'out_refund']),
            ('product_id.id', 'in', data['form']['product_ids']),
            ('move_id.invoice_date', '<=', data['form']['date_from']),
            ('move_id.invoice_date', '>=', data['form']['date_to']),
            ('move_id.partner_id.id', '=', data['form']['partner_id'][0]),
            ('move_id.invoice_user_id.id', '=', data['form']['salesman_id'][0])
        ]
        invoices = self.env['account.move.line'].search(domain)
        p = sum(invoices.mapped('unit_price'))
        print('my invoices', invoices)
        # credit_notes = self.env['account.move.line'].search(
        #     domain.append(('move_id.type', '=', 'out_refund')))
        # print('my credit notes', credit_notes)
        return {
            'doc_model': 'account.move',
            'data': data,
            'invoices': invoices
        }

from odoo import fields, models, api


class CustomerInvoicesRepoert(models.AbstractModel):
    _name = 'report.nakham_product_profit_report.purchase_details_tmpl'

    @api.model
    def _get_report_values(self, docids, data=None):
        # get data
        # print(data['form']['product_ids'])
        # print(data['form']['date_from'])
        # print(data['form']['date_to'])
        # print(data['form']['partner_id'])
        # print(data['form']['salesman_id'])

        domain = [
            ('move_id.type', 'in', ['out_invoice', 'out_refund']),
            ('account_id', '=', 19)]
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

        lines = self.env['account.move.line'].search(domain, order='product_id')
        lines_dict = []
        account_type_id = self.env.ref('account.data_account_type_direct_costs')
        total_total_price = 0.0
        total_total_cost = 0.0
        total_total_profit = 0.0
        total_quantity = 0.0
        for line in lines:
            domain = [
                ('move_id.id', '=', line.move_id.id),
                ('exclude_from_invoice_tab', '=', True),
                ('name', '=', line.name),
                ('account_id.user_type_id.id', '=', account_type_id.id)
            ]
            move_type = line.move_id.type
            line_ids = self.env['account.move.line'].search(domain)
            if line.move_id.type == 'out_invoice':
                total_cost = sum(line_ids.mapped('debit')) or 0.0
            else:
                total_cost = sum(line_ids.mapped('credit')) or 0.0
                total_cost *= -1

            lines_dict.append({
                'ref': line.move_id.name,
                'invoice_date': line.move_id.invoice_date,
                'product': line.product_id.name,
                'uom': line.product_uom_id.name,
                'quantity': line.quantity,
                'total_price': line.price_unit * line.quantity,
                'total_cost': total_cost,
                'total_profit': (line.price_unit * line.quantity) - total_cost
            })
            total_quantity += line.quantity
            total_total_price += line.price_unit * line.quantity
            total_total_cost += total_cost
            total_total_profit += (line.price_unit * line.quantity) - total_cost

        # price_subtotal_total = sum(invoices.mapped('price_subtotal'))
        # quantity_total = sum(invoices.mapped('quantity'))
        # total_price_unit = sum(invoices.mapped('price_unit'))
        # total_cost = sum(invoices.mapped('purchase_price'))
        # print('type of invoices', type(invoices))
        # print(total_price_unit)
        # print(total_cost)

        # print('my invoices', invoices)
        return {
            'doc_model': 'account.move',
            'data': data,
            'lines': lines_dict,
            'total_quantity': total_quantity,
            'total_total_price': total_total_price,
            'total_total_cost': total_total_cost,
            'total_total_profit': total_total_profit
        }

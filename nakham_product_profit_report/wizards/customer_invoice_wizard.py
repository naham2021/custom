from odoo import api, models, fields


class CustomerInvoiceReportWizard(models.TransientModel):
    _name = 'nakham.customer.invoice.report.wizard'

    product_ids = fields.Many2many('product.product', string="Products")
    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date To")
    partner_id = fields.Many2one('res.partner', 'Customer')
    salesman_id = fields.Many2one('res.users', 'Salesman')

    def print_report(self):
        data = {
            'model': 'nakham.customer.invoice.report.wizard',
            'form': self.read()[0]
        }
        print(self.read()[0])
        return self.env.ref('nakham_product_profit_report.nakham_report_customer_invoices').report_action(self,
                                                                                                          data=data)

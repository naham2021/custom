from odoo import api, models, fields
from odoo.exceptions import ValidationError


class CustomerInvoiceReportWizard(models.TransientModel):
    _name = 'nakham.customer.invoice.report.wizard'

    product_ids = fields.Many2many('product.product', string="Products")
    date_from = fields.Date(string="Date From", required=True)
    date_to = fields.Date(string="Date To", required=True)
    partner_id = fields.Many2one('res.partner', 'Customer', required=True)
    salesman_id = fields.Many2one('res.users', 'Salesman', required=True)

    @api.constrains('date_to')
    def _check_date_to(self):
        if self.date_to and self.date_from and self.date_from > self.date_to:
            raise ValidationError("Date To must be greater than Date From")

    def print_report(self):
        data = {
            'model': 'nakham.customer.invoice.report.wizard',
            'form': self.read()[0]
        }
        print(self.read()[0])
        return self.env.ref('nakham_product_profit_report.nakham_report_customer_invoices').report_action(self,
                                                                                                          data=data)

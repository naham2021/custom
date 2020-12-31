from odoo import api, models, fields
from odoo.osv import osv
import odoo.addons.decimal_precision as dp


class AccountInvoice(models.Model):
    _inherit = "account.move"

    discount_type = fields.Selection(selection=[('1', 'percentage'),
                                                ('2', 'Amount'), ('3', 'Per Line')],
                                     string='Discount Type')

    discount_rate = fields.Float(string='Discount Rate', digits_compute=dp.get_precision('Account'),
                                 readonly=True,
                                 states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, )

    amount_discount = fields.Float(digits_compute=dp.get_precision('Account'), string='Discount',
                                   store=True, help="The total discount.")

    def compute_discount(self, discount):
        for inv in self:
            val1 = val2 = 0.0
            disc_amnt = 0.0
            # val2 = sum(tax.amount for tax in line.tax_ids for line in self.invoice_line_ids)
            amount_untaxed = 0.0
            for line in inv.invoice_line_ids:
                for tax in line.tax_ids:
                    val2 += tax.amount * line.price_unit / 100
                val1 += (line.quantity * line.price_unit)
                line.discount = discount
                disc_amnt += (line.quantity * line.price_unit) * discount / 100
                line.price_subtotal = val1 - disc_amnt
                amount_untaxed += line.price_subtotal
            total = val1 + val2 - disc_amnt
            self.amount_discount = disc_amnt
            self.amount_tax = val2
            self.amount_total = total
            self.amount_untaxed = amount_untaxed

    def compute_discount_per_line(self):
        print('hi')
        for inv in self:
            val1 = val2 = 0.0
            disc_amnt = 0.0
            amount_untaxed = 0.0
            # val2 = sum(line.amount_total for line in self.tax_ids)
            for line in inv.invoice_line_ids:
                for tax in line.tax_ids:
                    val2 += tax.amount * line.price_unit / 100
                val1 += (line.quantity * line.price_unit)
                disc_amnt += (line.quantity * line.price_unit) * line.discount / 100
                line.price_subtotal = val1 - disc_amnt
                amount_untaxed += line.price_subtotal
            total = val1 + val2 - disc_amnt
            self.amount_discount = disc_amnt
            self.amount_tax = val2
            self.amount_total = total
            self.amount_untaxed = amount_untaxed

    @api.onchange('discount_type', 'discount_rate')
    def supply_rate(self):
        for inv in self:
            if not inv.discount_type and not inv.discount_type == '3':
                inv.discount_rate = 0
                self.compute_discount(0)
            else:
                if inv.discount_type == '1':
                    self.compute_discount(inv.discount_rate)
                elif inv.discount_type == '2':
                    total = 0.0
                    discount = 0.0
                    for line in inv.invoice_line_ids:
                        total += (line.quantity * line.price_unit)
                    if total > 0:
                        discount = (inv.discount_rate / total) * 100
                    self.compute_discount(discount)
                elif inv.discount_type == '3':
                    inv.discount_rate = 0
                    self.compute_discount_per_line()

    @api.model
    def _prepare_refund(self, invoice, date_invoice=None, date=None, description=None, journal_id=None):
        res = super(AccountInvoice, self)._prepare_refund(invoice, date_invoice=None, date=None, description=None,
                                                          journal_id=None)
        res.update({
            'discount_type': self.discount_type,
            'discount_rate': self.discount_rate,
        })
        return res

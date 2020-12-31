from odoo import models, fields, api,_,exceptions

class account_invoice(models.Model):
    _inherit = 'account.move'

    journal_ids = fields.Many2many('account.journal',string='Payment Journals',compute='compute_journal_ids')

    journal_id_name = fields.Char(string="Payment Method", required=False,compute='compute_journal_ids' )
    def compute_journal_ids(self):

        for rec in self:
            journals = []
            print('rec.id :: ',rec.id)
            pos_order = self.env['pos.order'].search([('name', '=',
                                                       rec.ref)])

            sale_order = self.env['sale.order'].search([('name', '=',
                                                         rec.ref)])
            if pos_order:
                print("pos_order")
                rec.journal_id_name = ''
                for order in pos_order.payment_ids:
                    rec.journal_id_name = order.payment_method_id.name
                    break
                rec.journal_ids = [(6, 0, [])]

            elif sale_order:
                print("sale_order")

                payments = self.env['account.payment'].search([('state', 'in', ['reconciled', 'sent', 'posted'])])
                print("payments :: ", payments.ids)
                print("payments :: ", len(payments))
                #     if rec.id in line.reconciled_invoice_ids.ids:
                #         journals.append(line.journal_id.id)
                for line in payments:
                    if rec.id in line.reconciled_invoice_ids.ids:
                        journals.append(line.journal_id.id)
                rec.journal_ids = [(6, 0, [])]
                rec.journal_id_name = ''
                if journals:
                    rec.journal_ids = journals
                    print("journals", journals)
                    journals_name = self.env['account.journal'].search([('id', 'in', journals)])

                    for j in journals_name:
                        rec.journal_id_name = j.name
                        break
                else:
                    rec.journal_ids = [(6, 0, [])]
                    rec.journal_id_name = ''
            else:
                rec.journal_ids = [(6, 0, [])]
                rec.journal_id_name = ''
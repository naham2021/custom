# -*- coding: utf-8 -*-

import base64

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    @api.depends('invoice_line_ids.discount', 'invoice_line_ids.price_unit', 'invoice_line_ids.quantity')
    def _cal_total_discount(self):
        for rec in self:
            total_discount = 0.0
            for line in rec.invoice_line_ids:
                total_discount += round(line.price_unit * line.quantity * line.discount / 100, 2)
            print(total_discount)
            rec.total_discount = total_discount
    total_discount = fields.Monetary(compute="_cal_total_discount")

    l10n_sa_delivery_date = fields.Date(string='Delivery Date', default=fields.Date.context_today, copy=False)
    l10n_sa_show_delivery_date = fields.Boolean(compute='_compute_show_delivery_date')
    l10n_sa_qr_code_str = fields.Char(string='Zatka QR Code', compute='_compute_qr_code_str')
    l10n_sa_confirmation_datetime = fields.Datetime(string='Confirmation Date', copy=False,readonly=True,default=fields.Datetime.now())

    @api.depends('company_id.country_id.code', 'type')
    def _compute_show_delivery_date(self):
        for move in self:
            move.l10n_sa_show_delivery_date = move.company_id.country_id.code == 'SA' and move.type in ('out_invoice', 'out_refund')

    @api.depends('amount_total', 'amount_untaxed', 'l10n_sa_confirmation_datetime', 'company_id', 'company_id.vat')
    def _compute_qr_code_str(self):
        """ Generate the qr code for Saudi e-invoicing. Specs are available at the following link at page 23
        https://zatca.gov.sa/ar/E-Invoicing/SystemsDevelopers/Documents/20210528_ZATCA_Electronic_Invoice_Security_Features_Implementation_Standards_vShared.pdf
        """
        def get_qr_encoding(tag, field):
            company_name_byte_array = field.encode('UTF-8')
            company_name_tag_encoding = tag.to_bytes(length=1, byteorder='big')
            company_name_length_encoding = len(company_name_byte_array).to_bytes(length=1, byteorder='big')
            return company_name_tag_encoding + company_name_length_encoding + company_name_byte_array

        for record in self:
            qr_code_str = ''
            if record.l10n_sa_confirmation_datetime and record.company_id.vat:
                seller_name_enc = get_qr_encoding(1, record.company_id.display_name)
                company_vat_enc = get_qr_encoding(2, record.company_id.vat)
                time_sa = fields.Datetime.context_timestamp(self.with_context(tz='Asia/Riyadh'), record.l10n_sa_confirmation_datetime)
                timestamp_enc = get_qr_encoding(3, time_sa.isoformat())
                invoice_total_enc = get_qr_encoding(4, str(record.amount_total))
                total_vat_enc = get_qr_encoding(5, str(record.currency_id.round(record.amount_total - record.amount_untaxed)))

                str_to_encode = seller_name_enc + company_vat_enc + timestamp_enc + invoice_total_enc + total_vat_enc
                qr_code_str = base64.b64encode(str_to_encode).decode('UTF-8')
            record.l10n_sa_qr_code_str = qr_code_str

    def post(self):
        res = super().post()
        for record in self:
            print('kkkkk',record.company_id.country_id.code)
            if record.company_id.country_id.code == 'SA' and record.type in ('out_invoice', 'out_refund'):
                if not record.l10n_sa_show_delivery_date:
                    raise UserError(_('Delivery Date cannot be empty'))
                if record.l10n_sa_delivery_date < record.invoice_date:
                    raise UserError(_('Delivery Date cannot be before Invoice Date'))
                record.write({
                    'l10n_sa_confirmation_datetime': fields.Datetime.now()
                })
        return res


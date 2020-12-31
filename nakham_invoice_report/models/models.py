# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo import models, fields, api, _, tools
import logging

_logger = logging.getLogger(__name__)

try:
    from num2words import num2words
except ImportError:
    _logger.warning("The num2words python library is not installed, amount-to-text features won't be fully available.")
    num2words = None

class ResCurrencyInherit(models.Model):
    _inherit = 'res.currency'



    def ar_amount_to_text(self, amount):
        self.ensure_one()

        def _num2words(number, lang):
            try:
                return num2words(number, lang=lang).title()
            except NotImplementedError:
                return num2words(number, lang='ar_SY').title()
        # def _num2words(number, lang):
        #     return num2words(number, lang=lang).title()


        if num2words is None:
            logging.getLogger(__name__).warning("The library 'num2words' is missing, cannot render textual amounts.")
            return ""

        formatted = "%.{0}f".format(self.decimal_places) % amount
        parts = formatted.partition('.')
        integer_value = int(parts[0])
        fractional_value = int(parts[2] or 0)

        lang_code = 'ar_SY'
        lang = self.env['res.lang'].with_context(active_test=False).search([('code', '=', lang_code)])
        _logger.info("lang :: ",lang)
        _logger.info("lang.iso_code :: ",lang.iso_code)
        amount_words = tools.ustr('{amt_value} {amt_word}').format(
            amt_value=_num2words(integer_value, lang=lang.iso_code),
            amt_word='ريال فقط لا غير' if self.is_zero(amount - integer_value) else 'ريال',
        )
        if not self.is_zero(amount - integer_value):
            amount_words += ' ' + _('و') + tools.ustr(' {amt_value} {amt_word}').format(
                amt_value=_num2words(fractional_value, lang=lang.iso_code),
                amt_word= 'هللة فقط لا غير' if fractional_value > 10 else 'هللات فقط لا غير ',
            )
        return amount_words

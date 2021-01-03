# -*- coding: utf-8 -*-

from odoo import models, fields, api

class accountmove(models.Model):
    _inherit = 'account.move'

    def my_button_cancel(self):
        for rec in self :
            rec.state = "draft"


class accountJournal(models.Model):
    _inherit = 'account.journal'

    update_posted = fields.Boolean(string='Allow Cancelling Entries',
                                   help="Check this box if you want to allow the cancellation the entries related to this journal or of the invoice related to this journal")

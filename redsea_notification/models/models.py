# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError, ValidationError

class account_move(models.Model):
    _inherit = 'account.move'

    # request_post = fields.Float(string="",  required=False, )
    is_request_post = fields.Boolean(string="Request", default=False )
    def request_to_post_account_move(self):
        for rec in self:
            rec.is_request_post = True
            group_advisor = self.env.ref('account.group_account_manager')

            mes = ("Please Check This  ( %s )  ") % (
                self.name)
            self.message_post(body="This", subtype='mt_comment',
                              partner_ids=[user.partner_id.id for user in group_advisor.users])

    # def action_post(self):
    #     res = super(account_move, self).action_post()
    #     partner = self.env['res.partner'].search([('id', '=', self.partner_id.id)], limit=1).sudo()
    #     group_advisor = self.env.ref('account.group_account_manager')
    #     print("group_advisor ",group_advisor)
    #     # partner_ids = self.get_partners(group_advisor)
    #     print("partner_ids user ",group_advisor.users)
    #     for partner in group_advisor.users:
    #         message = self.env['mail.message'].create({
    #             'subject': 'validation',
    #             'body': "validation Invoice" + self.name,
    #             'author_id': partner.partner_id.id,
    #             # 'needaction_partner_ids': [(4, partner.partner_id.id)],
    #             # 'email_from': self.env.company.l10n_it_address_send_fatturapa,
    #             # 'reply_to': self.env.company.l10n_it_address_send_fatturapa,
    #             # 'mail_server_id': self.env.company.l10n_it_mail_pec_server_id.id,
    #             # 'attachment_ids': [(6, 0, self.l10n_it_einvoice_id.ids)],
    #         })
    #         print("message",message)
    #         # self.env['mail.message'].create({'message_type': "notification",
    #         #                                  "subtype": self.env.ref("mail.mt_comment").id,
    #         #                                  'body': "validation Invoice" + self.name,
    #         #                                  'subject': "validation",
    #         #                                  'needaction_partner_ids': [
    #         #                                      (4, partner)],
    #         #                                  'model': self._name,
    #         #                                  # 'res_id': self.id,
    #         #                                  })
    #     mes = ("Please Check This  ( %s )  ") % (
    #                     self.name)
    #     self.message_post(body="This", subtype='mt_comment',
    #                                  partner_ids=[user.partner_id.id for user in group_advisor.users])
    #
    #     # raise ValidationError(_('Sorry stop here'))
    #
    #     return res

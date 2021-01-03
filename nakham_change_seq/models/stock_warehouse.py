# -*- coding: utf-8 -*-
from odoo import models, fields, api,_
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class stockwarehouseInherite(models.Model):
    _inherit = "stock.warehouse"

    analytic_account_id = fields.Many2one(comodel_name="account.analytic.account", string="Analytic Account", required=False, )
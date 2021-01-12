# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import copy
import json
import io
import logging
import lxml.html
import datetime
import ast
from collections import defaultdict
from math import copysign

from dateutil.relativedelta import relativedelta

from odoo.tools.misc import xlsxwriter
from odoo import models, fields, api, _
from odoo.tools import config, date_utils, get_lang
from odoo.osv import expression
from babel.dates import get_quarter_names
from odoo.tools.misc import formatLang, format_date
from odoo.addons.web.controllers.main import clean_action
from odoo.tools.safe_eval import safe_eval

_logger = logging.getLogger(__name__)


class AccountReportInherit(models.AbstractModel):
    _inherit = 'account.report'

    @api.model
    def _query_get(self, options, domain=None):
        print("_query_get :: ",options)
        print("_query_get :: ",domain)
        domain = self._get_options_domain(options) + (domain or [])
        self.env['account.move.line'].check_access_rights('read')

        query = self.env['account.move.line']._where_calc(domain)

        # Wrap the query with 'company_id IN (...)' to avoid bypassing company access rights.
        # self.env['account.move.line']._apply_ir_rules(query)

        return query.get_sql()

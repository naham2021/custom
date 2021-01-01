# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import copy
import ast

from odoo import models, fields, api, _
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import formatLang
from odoo.tools import float_is_zero, ustr
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression
#from odoo.tools.pycompat import izip #omara stopped


class ReportAccountFinancialReport(models.Model):
    _inherit = "account.financial.html.report"

    @api.model
    def _get_options(self, previous_options=None):
        if self.date_range:
            self.filter_date = {'date_from': '', 'date_to': '', 'filter': 'this_year'}
            if self.comparison:
                self.filter_comparison = {'date_from': '', 'date_to': '', 'filter': 'no_comparison', 'number_period': 1}
        else:
            self.filter_date = {'date': '', 'filter': 'today'}
            if self.comparison:
                self.filter_comparison = {'date': '', 'filter': 'no_comparison', 'number_period': 1}
        self.filter_cash_basis = False if self.cash_basis else None
        if self.unfold_all_filter:
            self.filter_unfold_all = False
        if self.show_journal_filter:
            self.filter_journals = True
        self.filter_all_entries = False
        self.filter_analytic = self.analytic or None
        if self.analytic:
            self.filter_analytic_accounts = [] if self.env.user.id in self.env.ref('analytic.group_analytic_accounting').users.ids else None
            self.filter_analytic_tags = [] if self.env.user.id in self.env.ref('analytic.group_analytic_tags').users.ids else None
            self.filter_analytic_groups = [] if self.env.user.id in self.env.ref('analytic.group_analytic_tags').users.ids else None
            #don't display the analytic filtering options if no option would be shown
            if self.filter_analytic_accounts is None and self.filter_analytic_tags is None and self.filter_analytic_groups is None:
                self.filter_analytic = None
        self.filter_hierarchy = True if self.hierarchy_option else None
        self.filter_ir_filters = self.applicable_filters_ids or None

        rslt = super(ReportAccountFinancialReport, self)._get_options(previous_options)

        # If manual values were stored in the context, we store them as options.
        # This is useful for report printing, were relying only on the context is
        # not enough, because of the use of a route to download the report (causing
        # a context loss, but keeping the options).
        if self.env.context.get('financial_report_line_values'):
            rslt['financial_report_line_values'] = self.env.context['financial_report_line_values']

        return rslt





    def _get_filter_info(self, options):
        if not options['ir_filters']:
            return False, False

        selected_ir_filter = [f for f in options['ir_filters'] if f.get('selected')]
        if selected_ir_filter:
            selected_ir_filter = selected_ir_filter[0]
        else:
            return False, False

        domain = ast.literal_eval(selected_ir_filter['domain'])
        group_by = ast.literal_eval(selected_ir_filter['context']).get('group_by', [])
        return domain, group_by

    #@api.multi omara stopped
    def _get_lines(self, options, line_id=None):
        line_obj = self.line_ids
        if line_id:
            line_obj = self.env['account.financial.html.report.line'].search([('id', '=', line_id)])
        if options.get('comparison') and options.get('comparison').get('periods'):
            line_obj = line_obj.with_context(periods=options['comparison']['periods'])
        if options.get('ir_filters'):
            line_obj = line_obj.with_context(periods=options.get('ir_filters'))

        currency_table = self._get_currency_table()
        domain, group_by = self._get_filter_info(options)
        if options.get('analytic_groups'):
            int_analytic_ids = []
            for item in options.get('analytic_groups'):
                int_analytic_ids.append(int(item))
                domain = [['analytic_group_ids','in',int_analytic_ids]]


        if group_by:
            options['groups'] = {}
            options['groups']['fields'] = group_by
            options['groups']['ids'] = self._get_groups(domain, group_by)

        amount_of_periods = len((options.get('comparison') or {}).get('periods') or []) + 1
        amount_of_group_ids = len(options.get('groups', {}).get('ids') or []) or 1
        linesDicts = [[{} for _ in range(0, amount_of_group_ids)] for _ in range(0, amount_of_periods)]

        res = line_obj.with_context(
            cash_basis=options.get('cash_basis'),
            filter_domain=domain,
        )._get_lines(self, currency_table, options, linesDicts)
        return res


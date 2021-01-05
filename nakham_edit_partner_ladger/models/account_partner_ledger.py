# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, api, _, _lt, fields
from odoo.tools.misc import format_date
from datetime import timedelta

from collections import defaultdict

class ReportPartnerLedger(models.AbstractModel):
    _inherit = "account.partner.ledger"


    @api.model
    def _get_lines_without_partner(self, options, expanded_partner=None, offset=0, limit=0):
        ''' Get the detail of lines without partner reconciled with a line with a partner. Those lines should be
        considered as belonging the partner for the reconciled amount as it may clear some of the partner invoice/bill
        and they have to be accounted in the partner balance.'''

        params = []
        if expanded_partner:
            partner_clause = '= %s'
            params = [expanded_partner.id] + params
        else:
            partner_clause = 'IS NOT NULL'
        new_options = self._get_options_without_partner(options)
        params += [options['date']['date_from'], options['date']['date_to']]
        tables, where_clause, where_params = self._query_get(new_options, domain=[])
        params += where_params + [offset]
        limit_clause = ''
        if limit != 0:
            params += [limit]
            limit_clause = "LIMIT %s"
        if options['partner_ids']:
            query = '''
            SELECT
                account_move_line.id,
                account_move_line.date,
                account_move_line.date_maturity,
                account_move_line.name,
                account_move_line.ref,
                account_move_line.company_id,
                account_move_line.account_id,
                account_move_line.payment_id,
                aml_with_partner.partner_id,
                account_move_line.currency_id,
                account_move_line.amount_currency,
                CASE WHEN aml_with_partner.balance > 0 THEN 0 ELSE partial.amount END AS debit,
                CASE WHEN aml_with_partner.balance < 0 THEN 0 ELSE partial.amount END AS credit,
                CASE WHEN aml_with_partner.balance > 0 THEN -partial.amount ELSE partial.amount END AS balance,
                account_move_line__move_id.name         AS move_name,
                account_move_line__move_id.type         AS move_type,
                account.code                            AS account_code,
                account.name                            AS account_name,
                journal.code                            AS journal_code,
                journal.name                            AS journal_name,
                full_rec.name                           AS full_rec_name
            FROM {tables},
                account_partial_reconcile partial
                LEFT JOIN account_full_reconcile full_rec ON full_rec.id = partial.full_reconcile_id,
                account_move_line aml_with_partner,
                account_journal journal,
                account_account account
            WHERE (account_move_line.id = partial.debit_move_id OR account_move_line.id = partial.credit_move_id)
               AND (aml_with_partner.id = partial.debit_move_id OR aml_with_partner.id = partial.credit_move_id)
               AND aml_with_partner.partner_id {partner_clause}
               AND journal.id = account_move_line.journal_id
               AND account.id = account_move_line.account_id
               AND partial.max_date BETWEEN %s AND %s
               AND {where_clause}
            ORDER BY account_move_line.date
            OFFSET %s
            {limit_clause}
        '''.format(tables=tables, partner_clause=partner_clause, where_clause=where_clause, limit_clause=limit_clause)
        else:
            query = '''
                SELECT
                    account_move_line.id,
                    account_move_line.date,
                    account_move_line.date_maturity,
                    account_move_line.name,
                    account_move_line.ref,
                    account_move_line.company_id,
                    account_move_line.account_id,
                    account_move_line.payment_id,
                    aml_with_partner.partner_id,
                    account_move_line.currency_id,
                    account_move_line.amount_currency,
                    CASE WHEN aml_with_partner.balance > 0 THEN 0 ELSE partial.amount END AS debit,
                    CASE WHEN aml_with_partner.balance < 0 THEN 0 ELSE partial.amount END AS credit,
                    CASE WHEN aml_with_partner.balance > 0 THEN -partial.amount ELSE partial.amount END AS balance,
                    account_move_line__move_id.name         AS move_name,
                    account_move_line__move_id.type         AS move_type,
                    account.code                            AS account_code,
                    account.name                            AS account_name,
                    journal.code                            AS journal_code,
                    journal.name                            AS journal_name,
                    full_rec.name                           AS full_rec_name
                FROM {tables},
                    account_partial_reconcile partial
                    LEFT JOIN account_full_reconcile full_rec ON full_rec.id = partial.full_reconcile_id,
                    account_move_line aml_with_partner,
                    account_journal journal,
                    account_account account
                WHERE (account_move_line.id = partial.debit_move_id OR account_move_line.id = partial.credit_move_id)
                   AND account_move_line.partner_id IS NULL
                   AND (aml_with_partner.id = partial.debit_move_id OR aml_with_partner.id = partial.credit_move_id)
                   AND aml_with_partner.partner_id {partner_clause}
                   AND journal.id = account_move_line.journal_id
                   AND account.id = account_move_line.account_id
                   AND partial.max_date BETWEEN %s AND %s
                   AND {where_clause}
                ORDER BY account_move_line.date
                OFFSET %s
                {limit_clause}
            '''.format(tables=tables, partner_clause=partner_clause, where_clause=where_clause,
                       limit_clause=limit_clause)

        return query, params

    @api.model
    def _get_sums_without_partner(self, options, expanded_partner=None):
        ''' Get the sum of lines without partner reconciled with a line with a partner, grouped by partner. Those lines
        should be considered as belonging the partner for the reconciled amount as it may clear some of the partner
        invoice/bill and they have to be accounted in the partner balance.'''

        params = []
        if expanded_partner:
            partner_clause = '= %s'
            params = [expanded_partner.id]
        else:
            partner_clause = 'IS NOT NULL'

        new_options = self._get_options_without_partner(options)
        params = [options['date']['date_from']] + params + [options['date']['date_to']]
        tables, where_clause, where_params = self._query_get(new_options, domain=[])
        params += where_params

        if options['partner_ids']:
            query = '''
            SELECT
                aml_with_partner.partner_id AS groupby,
                SUM(CASE WHEN aml_with_partner.balance > 0 THEN 0 ELSE partial.amount END) AS debit,
                SUM(CASE WHEN aml_with_partner.balance < 0 THEN 0 ELSE partial.amount END) AS credit,
                SUM(CASE WHEN aml_with_partner.balance > 0 THEN -partial.amount ELSE partial.amount END) AS balance,
                CASE WHEN partial.max_date < %s THEN 'initial_balance' ELSE 'sum' END as key
            FROM {tables}, account_partial_reconcile partial, account_move_line aml_with_partner
            WHERE (account_move_line.id = partial.debit_move_id OR account_move_line.id = partial.credit_move_id)
               AND (aml_with_partner.id = partial.debit_move_id OR aml_with_partner.id = partial.credit_move_id)
               AND aml_with_partner.partner_id {partner_clause}
               AND partial.max_date <= %s
               AND {where_clause}
            GROUP BY aml_with_partner.partner_id, key
        '''.format(tables=tables, partner_clause=partner_clause, where_clause=where_clause)
        else:
            query = '''
                SELECT
                    aml_with_partner.partner_id AS groupby,
                    SUM(CASE WHEN aml_with_partner.balance > 0 THEN 0 ELSE partial.amount END) AS debit,
                    SUM(CASE WHEN aml_with_partner.balance < 0 THEN 0 ELSE partial.amount END) AS credit,
                    SUM(CASE WHEN aml_with_partner.balance > 0 THEN -partial.amount ELSE partial.amount END) AS balance,
                    CASE WHEN partial.max_date < %s THEN 'initial_balance' ELSE 'sum' END as key
                FROM {tables}, account_partial_reconcile partial, account_move_line aml_with_partner
                WHERE (account_move_line.id = partial.debit_move_id OR account_move_line.id = partial.credit_move_id)
                   AND account_move_line.partner_id IS NULL
                   AND (aml_with_partner.id = partial.debit_move_id OR aml_with_partner.id = partial.credit_move_id)
                   AND aml_with_partner.partner_id {partner_clause}
                   AND partial.max_date <= %s
                   AND {where_clause}
                GROUP BY aml_with_partner.partner_id, key
            '''.format(tables=tables, partner_clause=partner_clause, where_clause=where_clause)

        return query, params

    # @api.model
    # def _get_sums_without_partner(self, options, expanded_partner=None):
    #     ''' Get the sum of lines without partner reconciled with a line with a partner, grouped by partner. Those lines
    #     should be considered as belonging the partner for the reconciled amount as it may clear some of the partner
    #     invoice/bill and they have to be accounted in the partner balance.'''
    #     # print("_get_sums_without_partner")
    #     params = []
    #     if expanded_partner:
    #         partner_clause = '= %s'
    #         params = [expanded_partner.id]
    #     else:
    #         partner_clause = 'IS NOT NULL'
    #
    #     new_options = self._get_options_without_partner(options)
    #     params = [options['date']['date_from']] + params + [options['date']['date_to']]
    #     tables, where_clause, where_params = self._query_get(new_options, domain=[])
    #     params += where_params
    #     if options['partner_ids']:
    #         query = '''
    #         SELECT
    #             aml_with_partner.partner_id AS groupby,
    #             SUM(CASE WHEN aml_with_partner.balance > 0 THEN 0 ELSE partial.amount END) AS debit,
    #             SUM(CASE WHEN aml_with_partner.balance < 0 THEN 0 ELSE partial.amount END) AS credit,
    #             SUM(CASE WHEN aml_with_partner.balance > 0 THEN -partial.amount ELSE partial.amount END) AS balance,
    #             CASE WHEN partial.max_date < %s THEN 'initial_balance' ELSE 'sum' END as key
    #         FROM {tables}, account_partial_reconcile partial, account_move_line aml_with_partner
    #         WHERE (account_move_line.id = partial.debit_move_id OR account_move_line.id = partial.credit_move_id)
    #            AND (aml_with_partner.id = partial.debit_move_id OR aml_with_partner.id = partial.credit_move_id)
    #            AND aml_with_partner.partner_id {partner_clause}
    #            AND partial.max_date <= %s
    #            AND {where_clause}
    #         GROUP BY aml_with_partner.partner_id, key
    #     '''.format(tables=tables, partner_clause=partner_clause, where_clause=where_clause)
    #     else:
    #         query = '''
    #             SELECT
    #                 aml_with_partner.partner_id AS groupby,
    #                 SUM(CASE WHEN aml_with_partner.balance > 0 THEN 0 ELSE partial.amount END) AS debit,
    #                 SUM(CASE WHEN aml_with_partner.balance < 0 THEN 0 ELSE partial.amount END) AS credit,
    #                 SUM(CASE WHEN aml_with_partner.balance > 0 THEN -partial.amount ELSE partial.amount END) AS balance,
    #                 CASE WHEN partial.max_date < %s THEN 'initial_balance' ELSE 'sum' END as key
    #             FROM {tables}, account_partial_reconcile partial, account_move_line aml_with_partner
    #             WHERE (account_move_line.id = partial.debit_move_id OR account_move_line.id = partial.credit_move_id)
    #                AND account_move_line.partner_id IS NULL
    #                AND (aml_with_partner.id = partial.debit_move_id OR aml_with_partner.id = partial.credit_move_id)
    #                AND aml_with_partner.partner_id {partner_clause}
    #                AND partial.max_date <= %s
    #                AND {where_clause}
    #             GROUP BY aml_with_partner.partner_id, key
    #         '''.format(tables=tables, partner_clause=partner_clause, where_clause=where_clause)
    #
    #     return query, params
















    # @api.model
    # def _get_lines_without_partner(self, options, expanded_partner=None, offset=0, limit=0):
    #     ''' Get the detail of lines without partner reconciled with a line with a partner. Those lines should be
    #     considered as belonging the partner for the reconciled amount as it may clear some of the partner invoice/bill
    #     and they have to be accounted in the partner balance.'''
    #     print("options :: ",options['partner_ids'])
    #
    #     params = []
    #     if expanded_partner:
    #         print("expanded_partner")
    #         partner_clause = '= %s'
    #         params = [expanded_partner.id] + params
    #     else:
    #         print("else expanded_partner")
    #
    #         # partner_clause = '= %s'
    #         # params = params
    #         # partner_clause = 'IS NOT NULL'
    #     new_options = self._get_options_without_partner(options)
    #     params += [options['date']['date_from'], options['date']['date_to']]
    #     tables, where_clause, where_params = self._query_get(new_options, domain=[])
    #     params += where_params + [offset]
    #     limit_clause = ''
    #     if limit != 0:
    #         params += [limit]
    #         limit_clause = "LIMIT %s"
    #
    #     if options['partner_ids']:
    #         query = '''
    #             SELECT
    #                 account_move_line.id,
    #                 account_move_line.date,
    #                 account_move_line.date_maturity,
    #                 account_move_line.name,
    #                 account_move_line.ref,
    #                 account_move_line.company_id,
    #                 account_move_line.account_id,
    #                 account_move_line.payment_id,
    #                 aml_with_partner.partner_id,
    #                 account_move_line.currency_id,
    #                 account_move_line.amount_currency,
    #                 CASE WHEN aml_with_partner.balance > 0 THEN 0 ELSE partial.amount END AS debit,
    #                 CASE WHEN aml_with_partner.balance < 0 THEN 0 ELSE partial.amount END AS credit,
    #                 CASE WHEN aml_with_partner.balance > 0 THEN -partial.amount ELSE partial.amount END AS balance,
    #                 account_move_line__move_id.name         AS move_name,
    #                 account_move_line__move_id.type         AS move_type,
    #                 account.code                            AS account_code,
    #                 account.name                            AS account_name,
    #                 journal.code                            AS journal_code,
    #                 journal.name                            AS journal_name,
    #                 full_rec.name                           AS full_rec_name
    #             FROM {tables},
    #                 account_partial_reconcile partial
    #                 LEFT JOIN account_full_reconcile full_rec ON full_rec.id = partial.full_reconcile_id,
    #                 account_move_line aml_with_partner,
    #                 account_journal journal,
    #                 account_account account
    #             WHERE (account_move_line.id = partial.debit_move_id OR account_move_line.id = partial.credit_move_id)
    #                AND (aml_with_partner.id = partial.debit_move_id OR aml_with_partner.id = partial.credit_move_id)
    #                AND journal.id = account_move_line.journal_id
    #                AND account.id = account_move_line.account_id
    #                AND partial.max_date BETWEEN %s AND %s
    #                AND {where_clause}
    #             ORDER BY account_move_line.date
    #             OFFSET %s
    #             {limit_clause}
    #         '''.format(tables=tables,  where_clause=where_clause, limit_clause=limit_clause)
    #     else:
    #         query = '''
    #                     SELECT
    #                         account_move_line.id,
    #                         account_move_line.date,
    #                         account_move_line.date_maturity,
    #                         account_move_line.name,
    #                         account_move_line.ref,
    #                         account_move_line.company_id,
    #                         account_move_line.account_id,
    #                         account_move_line.payment_id,
    #                         aml_with_partner.partner_id,
    #                         account_move_line.currency_id,
    #                         account_move_line.amount_currency,
    #                         CASE WHEN aml_with_partner.balance > 0 THEN 0 ELSE partial.amount END AS debit,
    #                         CASE WHEN aml_with_partner.balance < 0 THEN 0 ELSE partial.amount END AS credit,
    #                         CASE WHEN aml_with_partner.balance > 0 THEN -partial.amount ELSE partial.amount END AS balance,
    #                         account_move_line__move_id.name         AS move_name,
    #                         account_move_line__move_id.type         AS move_type,
    #                         account.code                            AS account_code,
    #                         account.name                            AS account_name,
    #                         journal.code                            AS journal_code,
    #                         journal.name                            AS journal_name,
    #                         full_rec.name                           AS full_rec_name
    #                     FROM {tables},
    #                         account_partial_reconcile partial
    #                         LEFT JOIN account_full_reconcile full_rec ON full_rec.id = partial.full_reconcile_id,
    #                         account_move_line aml_with_partner,
    #                         account_journal journal,
    #                         account_account account
    #                     WHERE (account_move_line.id = partial.debit_move_id OR account_move_line.id = partial.credit_move_id)
    #                        AND account_move_line.partner_id IS NULL
    #                        AND (aml_with_partner.id = partial.debit_move_id OR aml_with_partner.id = partial.credit_move_id)
    #                        AND journal.id = account_move_line.journal_id
    #                        AND account.id = account_move_line.account_id
    #                        AND partial.max_date BETWEEN %s AND %s
    #                        AND {where_clause}
    #                     ORDER BY account_move_line.date
    #                     OFFSET %s
    #                     {limit_clause}
    #                 '''.format(tables=tables, where_clause=where_clause, limit_clause=limit_clause)
    #
    #     return query, params

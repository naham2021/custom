# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.osv import expression
from odoo.osv.expression import get_unaccent_wrapper
import re
from odoo.addons.base.models import res_partner as ResPartner


class PartnerArea(models.Model):
    _name = 'partner.area'
    _rec_name = 'name'
    _description = 'Area'

    name = fields.Char()
    code = fields.Char(required=True)
    next_code_sequence = fields.Integer(default=1)
    area_customers = fields.Integer(string='Customers', compute='get_area_customers')

    _sql_constraints = [
        ('area_code_unique', 'UNIQUE(code)', 'Area Code must be unique.')
    ]

    def get_area_customers(self):
        for rec in self:
            rec.area_customers = len(self.env['res.partner'].search([('area_id', '=', rec.id)]))

    def get_customers(self):
        for rec in self:
            return {
                'name': 'Customers',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'res.partner',
                'type': 'ir.actions.act_window',
                'domain': [('area_id', '=', rec.id)],
                'context': {
                    'default_area_id': rec.id,
                }
            }

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if operator == "ilike" and not (name or "").strip():
            domain = []
        else:
            domain = [
                "|",
                ("name", operator, name),
                ("code", operator, name)
            ]
        rec = self._search(
            expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid
        )
        return models.lazy_name_get(self.browse(rec).with_user(name_get_uid))


class ResPartner(models.Model):
    _inherit = 'res.partner'

    area_id = fields.Many2one(comodel_name="partner.area")
    name_seq = fields.Char(string='Customer Reference', required=True, copy=False, readonly=True, index=True,
                           default=_('New'))


    @api.model
    def create(self, vals):
        print('in create')
        print(vals)
        if self._context.get('default_customer_rank') and vals.get('area_id'):
            # print('in customer')
            # if vals.get('area_id'):
            #     print('in area')
            #     current_area = self.env['partner.area'].sudo().search([('id', '=', vals.get('area_id'))])
            #     print('current area >> ', current_area)
            #     current_area_count = self.env['res.partner'].sudo().search_count([('area_id', '=', vals.get('area_id'))])
            #     print('current area count >> ', current_area)
            #     vals['name_seq'] = str(current_area.code) + '00' + str(current_area_count + 1)
            #     print('sequence >> ', vals['name_seq'])
            print('area ->>>>>>>>>>>>>>>>>>>>>>>>', vals.get('area_id'))
            area_id = self.env['partner.area'].browse(vals.get('area_id'))
            vals['name_seq'] = str(area_id.code) + str(area_id.next_code_sequence).rjust(5, '0')
            area_id.next_code_sequence += 1
        result = super(ResPartner, self).create(vals)
        return result

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        self = self.with_user(name_get_uid or self.env.uid)
        # as the implementation is in SQL, we force the recompute of fields if necessary
        self.recompute(['display_name'])
        self.flush()
        if args is None:
            args = []
        order_by_rank = self.env.context.get('res_partner_search_mode')
        if (name or order_by_rank) and operator in ('=', 'ilike', '=ilike', 'like', '=like'):
            self.check_access_rights('read')
            where_query = self._where_calc(args)
            self._apply_ir_rules(where_query, 'read')
            from_clause, where_clause, where_clause_params = where_query.get_sql()
            from_str = from_clause if from_clause else 'res_partner'
            where_str = where_clause and (" WHERE %s AND " % where_clause) or ' WHERE '

            # search on the name of the contacts and of its company
            search_name = name
            if operator in ('ilike', 'like'):
                search_name = '%%%s%%' % name
            if operator in ('=ilike', '=like'):
                operator = operator[1:]

            unaccent = get_unaccent_wrapper(self.env.cr)

            fields = self._get_name_search_order_by_fields()

            query = """SELECT res_partner.id
                             FROM {from_str}
                          {where} ({email} {operator} {percent}
                               OR {display_name} {operator} {percent}
                               OR {reference} {operator} {percent}
                               OR {vat} {operator} {percent}
                               OR {name_seq} {operator} {percent})
                               -- don't panic, trust postgres bitmap
                         ORDER BY {fields} {display_name} {operator} {percent} desc,
                                  {display_name}
                        """.format(from_str=from_str,
                                   fields=fields,
                                   where=where_str,
                                   operator=operator,
                                   email=unaccent('res_partner.email'),
                                   display_name=unaccent('res_partner.display_name'),
                                   reference=unaccent('res_partner.ref'),
                                   percent=unaccent('%s'),
                                   vat=unaccent('res_partner.vat'),
                                   name_seq=unaccent('res_partner.name_seq'), )

            where_clause_params += [search_name] * 4  # for email / display_name, reference , seq_name
            where_clause_params += [re.sub('[^a-zA-Z0-9]+', '', search_name) or None]  # for vat
            where_clause_params += [search_name]  # for order by
            if limit:
                query += ' limit %s'
                where_clause_params.append(limit)
            self.env.cr.execute(query, where_clause_params)
            partner_ids = [row[0] for row in self.env.cr.fetchall()]

            if partner_ids:
                return models.lazy_name_get(self.browse(partner_ids))
            else:
                return []
        return super(ResPartner, self)._name_search(name, args, operator=operator, limit=limit, name_get_uid=name_get_uid)

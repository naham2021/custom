# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError
import xlsxwriter
from io import BytesIO
import base64
from datetime import datetime
from odoo.osv import expression
from datetime import timedelta


class excelreport(models.TransientModel):
    _name = 'report.excel'

    excel_file = fields.Binary('Dowload report Excel', attachment=True, readonly=True)
    file_name = fields.Char('Excel File', size=64)


class qtytobepurchasedwizard(models.TransientModel):
    _name = 'qty.tobe.purchased.wizard'

    def _get_location_ids_domain(self):
        return [('id', 'in', self.env.user.allowed_bad_stock_location_ids.ids)]

    excel_file = fields.Binary('Download report Excel', attachment=True, readonly=True)
    file_name = fields.Char('Excel File', size=64)
    date_from = fields.Datetime(string="Date From")
    date_to = fields.Datetime(string="Date To")
    product_id = fields.Many2one('product.product', domain=[('type', 'in', ('product', 'consu'))], string="Product")
    product_categ_ids = fields.Many2many('product.category', string="Product Categ")
    number_of_month = fields.Integer(string="Number Of Month")
    search_by = fields.Selection([('product', 'Product'), ('categ', 'Product Categ')], string="Search By")
    computed_months = fields.Float(string='Computed Months', compute='compute_months')
    location_ids = fields.Many2many('stock.location', domain=_get_location_ids_domain)
    is_all_system = fields.Boolean(string="All System",  )
    @api.depends('date_from', 'date_to')
    def compute_months(self):
        for rec in self:
            if rec.date_from and rec.date_to:
                print((rec.date_to - rec.date_from).days)

                # date_from_month = rec.date_from.month
                # date_from_year = rec.date_from.year
                # date_to_month = rec.date_to.month
                # date_to_year = rec.date_to.year
                # rec.computed_months = date_to_month - date_from_month  + 12*(date_to_year - date_from_year)
                days = (rec.date_to - rec.date_from).days
                rec.computed_months = round(days / 30, 2)
            else:
                rec.computed_months = 0

    def qty_tobe_purchased_search(self):

        act = self.generate_excel()

        return {

            'type': 'ir.actions.act_window',
            'res_model': 'report.excel',
            'res_id': act.id,
            'view_type': 'form',
            'view_mode': 'form',
            'context': self.env.context,
            'target': 'new',

        }

    def generate_excel(self):

        filename = "Qty To Be Purchased"

        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Qty To Be Purchased')

        without_borders = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'text_wrap': True,
            'font_size': '11',

        })
        format0 = workbook.add_format({'font_size': 20, 'align': 'center', 'bold': True})
        format1 = workbook.add_format({'font_size': 10, 'align': 'center', 'bold': False})

        font_size_10 = workbook.add_format(
            {'font_name': 'KacstBook', 'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
             'border': 1})

        table_header_formate = workbook.add_format({
            'bold': 1,
            'border': 1,
            'bg_color': '#AAB7B8',
            'font_size': '10',
            'align': 'center',
            'valign': 'vcenter',
            'text_wrap': True
        })
        sheet.merge_range(1, 3, 2, 6, "Qty To Be Purchased", format0)
        sheet.merge_range(2, 7, 2, 8, "Date : " + str(datetime.today().strftime('%Y-%m-%d')), format1)

        sheet.set_column(4, 0, 9, without_borders)
        sheet.set_column(4, 9, 19, without_borders)
        sheet.write('A4', 'No', table_header_formate)
        sheet.write('B4', 'Product Code', table_header_formate)
        sheet.write('C4', 'Product Name', table_header_formate)
        sheet.write('D4', 'Product Categ', table_header_formate)
        sheet.write('E4', 'First Period', table_header_formate)
        sheet.write('F4', 'OnHand', table_header_formate)
        sheet.write('G4', 'Avg Monthly Sale', table_header_formate)
        sheet.write('H4', 'Needed Months', table_header_formate)
        sheet.write('I4', 'Qty To be Purchased', table_header_formate)

        row = 4
        seq = 1
        col = 0
        if self.search_by == 'product':
            products = self.env['product.product'].search(
                [('id', '=', self.product_id.id), ('type', 'in', ('product', 'consu'))])
        elif self.search_by == 'categ':
            products = self.env['product.product'].search(
                [('categ_id', 'in', self.product_categ_ids.ids), ('type', 'in', ('product', 'consu'))])
        else:
            products = self.env['product.product'].search([('type', 'in', ('product', 'consu'))])

        all_stock_move_of_period = self.env['stock.move.line'].search(
            [('state', '=', 'done'), ('date', '>=', self.date_from), ('date', '<=', self.date_to),
             ('product_id', 'in', products.ids)])

        # all System
        locations_all = self.env['stock.location'].search([('usage', '=', 'internal')])

        if self.is_all_system == True:
            for rec in products:
                print("product name : ",rec.name)
                product = rec.id
                domain = ([('id', '=', product)])
                first_balance = 0
                balance = 0
                qty_to = sum(self.env['stock.move.line'].search([
                    ('state', '=', 'done'),
                    ('date', '<', self.date_from),
                    ('product_id', '=', rec.id),
                    ('location_dest_id', 'in', locations_all.ids)
                ]).mapped('qty_done'))
                qty_from = sum(self.env['stock.move.line'].search([
                    ('state', '=', 'done'),
                    ('date', '<', self.date_from),
                    ('product_id', '=', rec.id),
                    ('location_id', '=', locations_all.ids)

                ]).mapped('qty_done'))
                first_balance += qty_to - qty_from
                balance_tmp = sum(self.env['stock.quant'].search([
                    ('product_id', '=', rec.id),
                    ('location_id', '=', locations_all.ids)

                ]).mapped('quantity'))
                balance += balance_tmp
                qty_avaiable = balance
                date_from_date = self.date_from.date()
                date_to_date = self.date_to.date()
                invcome_qty_to = sum(all_stock_move_of_period.filtered(lambda
                                                                           l: l.product_id.id == rec.id and l.location_id.id in locations_all.ids and l.location_dest_id.usage == 'customer').mapped(
                    'qty_done'))
                print("invcome_qty_to :> ",invcome_qty_to)
                invcome_qty_from = sum(all_stock_move_of_period.filtered(lambda
                                                                             l: l.product_id.id == rec.id and l.location_dest_id.id in locations_all.ids and l.location_id.usage == 'customer').mapped(
                    'qty_done'))
                print("invcome_qty_from :> ",invcome_qty_from)

                monsaref = invcome_qty_to - invcome_qty_from
                avg_monthly_sale = monsaref / self.computed_months
                needed_months = avg_monthly_sale * self.number_of_month



                sheet.write(row, col, str(seq) or '', font_size_10)
                sheet.write(row, col + 1, rec.default_code or '', font_size_10)
                sheet.write(row, col + 2, rec.name or '', font_size_10)
                sheet.write(row, col + 3, rec.categ_id.name or '', font_size_10)
                sheet.write(row, col + 4, round(first_balance, 2) or '0.0', font_size_10)
                sheet.write(row, col + 5, round(qty_avaiable, 2) or '0.0', font_size_10)
                sheet.write(row, col + 6, round(avg_monthly_sale, 2) or '0.0', font_size_10)
                sheet.write(row, col + 7, round(needed_months, 2) or '0.0', font_size_10)
                # sheet.write(row, col + 8, round(first_balance - needed_months, 2) or '0.0', font_size_10)
                sheet.write(row, col + 8, round(needed_months - qty_avaiable, 2) or '0.0', font_size_10)

                row += 1
                seq += 1
        else:
            for rec in products:
                print("product name : ",rec.name)
                product = rec.id
                domain = ([('id', '=', product)])
                # my_products = self.env['product.product'].search(domain).with_context(
                #     dict(self.env.context, to_date=self.date_from))
                #
                first_balance = 0
                balance = 0
                qty_avaiable_to = 0
                qty_avaiable_from = 0
                for location in self.location_ids:
                    print("location name : ", location.complete_name)

                    qty_to = sum(self.env['stock.move.line'].search([
                        ('state', '=', 'done'),
                        ('date', '<', self.date_from),
                        ('product_id', '=', rec.id),
                        ('location_dest_id', '=', location.id)
                    ]).mapped('qty_done'))
                    qty_from = sum(self.env['stock.move.line'].search([
                        ('state', '=', 'done'),
                        ('date', '<', self.date_from),
                        ('product_id', '=', rec.id),
                        ('location_id', '=', location.id)
                    ]).mapped('qty_done'))
                    first_balance += qty_to - qty_from
                    # qty_to = sum(self.env['stock.move.line'].search([
                    #     ('state', '=', 'done'),
                    #     ('date', '>=', self.date_from),
                    #     ('date', '<=', self.date_to),
                    #     ('product_id', '=', rec.id),
                    #     ('location_dest_id', '=', location.id)
                    # ]).mapped('qty_done'))
                    # qty_from = sum(self.env['stock.move.line'].search([
                    #     ('state', '=', 'done'),
                    #     ('date', '>=', self.date_from),
                    #     ('date', '<=', self.date_to),
                    #     ('product_id', '=', rec.id),
                    #     ('location_id', '=', location.id)
                    # ]).mapped('qty_done'))
                    # qty_avaiable_to += qty_to
                    # qty_avaiable_from += qty_from
                    balance_tmp = sum(self.env['stock.quant'].search([
                        ('product_id', '=', rec.id),
                        ('location_id', '=', location.id)
                    ]).mapped('quantity'))
                    balance += balance_tmp
                qty_avaiable = balance

                date_from_date = self.date_from.date()
                date_to_date = self.date_to.date()
                # invoices_qty = sum(self.env['account.move.line'].search([('date','>=',date_from_date),('date','<=',date_to_date),('parent_state','=','posted'),('product_id','=',rec.id),('move_id.type','=','out_invoice')]).mapped('quantity'))
                # credit_qty = sum(self.env['account.move.line'].search([('date','>=',date_from_date),('date','<=',date_to_date),('parent_state','=','posted'),('product_id','=',rec.id),('move_id.type','=','out_refund')]).mapped('quantity'))
                # invoices_qty = sum(self.env['stock.move.line'].search(
                #     [('date', '>=', date_from_date), ('date', '<=', date_to_date), ('state', '=', 'done'),
                #      ('product_id', '=', rec.id), ('location_dest_id.usage', '=', 'customer')]).mapped('qty_done'))
                # credit_qty = sum(self.env['stock.move.line'].search(
                #     [('date', '>=', date_from_date), ('date', '<=', date_to_date), ('state', '=', 'done'),
                #      ('product_id', '=', rec.id), ('location_id.usage', '=', 'customer')]).mapped('qty_done'))


                invcome_qty_to = sum(all_stock_move_of_period.filtered(lambda
                                                                           l: l.product_id.id == rec.id and l.location_id.id in self.location_ids.ids and l.location_dest_id.usage == 'customer').mapped(
                    'qty_done'))
                print("invcome_qty_to :> ",invcome_qty_to)
                invcome_qty_from = sum(all_stock_move_of_period.filtered(lambda
                                                                             l: l.product_id.id == rec.id and l.location_dest_id.id in self.location_ids.ids and l.location_id.usage == 'customer').mapped(
                    'qty_done'))
                print("invcome_qty_from :> ",invcome_qty_from)

                monsaref = invcome_qty_to - invcome_qty_from
                avg_monthly_sale = monsaref / self.computed_months
                needed_months = avg_monthly_sale * self.number_of_month



                sheet.write(row, col, str(seq) or '', font_size_10)
                sheet.write(row, col + 1, rec.default_code or '', font_size_10)
                sheet.write(row, col + 2, rec.name or '', font_size_10)
                sheet.write(row, col + 3, rec.categ_id.name or '', font_size_10)
                sheet.write(row, col + 4, round(first_balance, 2) or '0.0', font_size_10)
                sheet.write(row, col + 5, round(qty_avaiable, 2) or '0.0', font_size_10)
                sheet.write(row, col + 6, round(avg_monthly_sale, 2) or '0.0', font_size_10)
                sheet.write(row, col + 7, round(needed_months, 2) or '0.0', font_size_10)
                # sheet.write(row, col + 8, round(first_balance - needed_months, 2) or '0.0', font_size_10)
                sheet.write(row, col + 8, round(needed_months - qty_avaiable, 2) or '0.0', font_size_10)

                row += 1
                seq += 1

        workbook.close()
        output.seek(0)

        self.write({'file_name': filename + str(datetime.today().strftime('%Y-%m-%d')) + '.xlsx'})
        self.excel_file = base64.b64encode(output.read())

        context = {
            'file_name': self.file_name,
            'excel_file': self.excel_file,
        }

        act_id = self.env['report.excel'].create(context)
        return act_id

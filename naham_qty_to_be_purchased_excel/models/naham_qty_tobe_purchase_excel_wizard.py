# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError
import xlsxwriter
from io import BytesIO
import base64
from datetime import datetime
from odoo.osv import expression





class excelreport(models.TransientModel):
    _name = 'report.excel'

    excel_file = fields.Binary('Dowload report Excel', attachment=True, readonly=True)
    file_name = fields.Char('Excel File', size=64)




class qtytobepurchasedwizard(models.TransientModel):
    _name = 'qty.tobe.purchased.wizard'


    excel_file = fields.Binary('Download report Excel', attachment=True, readonly=True)
    file_name = fields.Char('Excel File', size=64)
    date_from = fields.Datetime(string="Date From")
    date_to = fields.Datetime(string="Date To")
    product_id = fields.Many2one('product.product',domain=[('type','in',('product','consu'))],string="Product")
    product_categ_ids = fields.Many2many('product.category',string="Product Categ")
    number_of_month = fields.Integer(string="Number Of Month")
    search_by = fields.Selection([('product','Product'),('categ','Product Categ')],string="Search By")
    computed_months = fields.Integer(string='Computed Months',compute='compute_months')

    @api.depends('date_from','date_to')
    def compute_months(self):
        for rec in self:
            if rec.date_from and rec.date_to:
                date_from_month = rec.date_from.month
                date_from_year = rec.date_from.year
                date_to_month = rec.date_to.month
                date_to_year = rec.date_to.year
                rec.computed_months = date_to_month - date_from_month  + 12*(date_to_year - date_from_year)

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
        sheet.merge_range(1, 3, 2, 6,"Qty To Be Purchased", format0)
        sheet.merge_range(2, 7, 2, 8,"Date : "+str(datetime.today().strftime('%Y-%m-%d')), format1)

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
            products = self.env['product.product'].search([('id', '=',self.product_id.id),('type', 'in', ('product', 'consu'))])
        elif self.search_by == 'categ':
            products = self.env['product.product'].search(
                [('categ_id', 'in', self.product_categ_ids.ids), ('type', 'in', ('product', 'consu'))])
        else:
            products = self.env['product.product'].search([('type', 'in', ('product', 'consu'))])



        for rec in products:
            product = rec.id
            domain = ([('id', '=', product)])
            my_products = self.env['product.product'].search(domain).with_context(
                dict(self.env.context, to_date=self.date_from))
            first_balance = my_products[0].qty_available

            date_from_date = self.date_from.date()
            date_to_date = self.date_to.date()
            invoices_qty = sum(self.env['account.move.line'].search([('date','>=',date_from_date),('date','<=',date_to_date),('parent_state','=','posted'),('product_id','=',rec.id),('move_id.type','=','out_invoice')]).mapped('quantity'))
            credit_qty = sum(self.env['account.move.line'].search([('date','>=',date_from_date),('date','<=',date_to_date),('parent_state','=','posted'),('product_id','=',rec.id),('move_id.type','=','out_refund')]).mapped('quantity'))
            # print('invoices_qty', invoices_qty)
            # print('credit_qty', credit_qty)
            # print('invoices_qty - credit_qty', invoices_qty - credit_qty)
            # print('computed_months', self.computed_months)
            avg_monthly_sale = (invoices_qty - credit_qty)/self.computed_months
            # avg_monthly_sale = 0.0
            needed_months = avg_monthly_sale * self.number_of_month


            sheet.write(row, col, str(seq) or '', font_size_10)
            sheet.write(row, col + 1, rec.default_code or '', font_size_10)
            sheet.write(row, col + 2, rec.name or '', font_size_10)
            sheet.write(row, col + 3, rec.categ_id.name or '', font_size_10)
            sheet.write(row, col + 4, first_balance or '', font_size_10)
            sheet.write(row, col + 5, rec.qty_available or '', font_size_10)
            sheet.write(row, col + 6, avg_monthly_sale or '', font_size_10)
            sheet.write(row, col + 7, needed_months or '', font_size_10)
            sheet.write(row, col + 8, rec.qty_available - needed_months or '', font_size_10)

            row += 1
            seq += 1




        workbook.close()
        output.seek(0)

        self.write({'file_name': filename + str(datetime.today().strftime('%Y-%m-%d')) + '.xlsx'})
        self.excel_file = base64.b64encode(output.read())

        context = {
            'file_name': self.file_name ,
            'excel_file': self.excel_file,
        }

        act_id = self.env['report.excel'].create(context)
        return act_id








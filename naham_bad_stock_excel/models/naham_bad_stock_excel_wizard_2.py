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




class badstockwizard(models.TransientModel):
    _name = 'bad.stock.wizard'


    excel_file = fields.Binary('Download report Excel', attachment=True, readonly=True)
    file_name = fields.Char('Excel File', size=64)
    date_from = fields.Datetime(string="Date From")
    date_to = fields.Datetime(string="Date To")
    product_id = fields.Many2one('product.product',domain=[('type','in',('product','consu'))],string="Product")
    product_categ_ids = fields.Many2many('product.category',string="Product Categ")
    location_id = fields.Many2one('stock.location',domain=[('usage','in',('internal','transit'))],string="Location")
    search_by = fields.Selection([('product','Product'),('categ','Product Categ')],string="Search By")

    def open_at_date(self,product,inventory_date):
        tree_view_id = self.env.ref('stock.view_stock_product_tree').id
        form_view_id = self.env.ref('stock.product_form_view_procurement_button').id
        domain = [('type', '=', 'product')]
        product_id = product
        if product_id:
            domain = expression.AND([domain, [('id', '=', product_id)]])

        action = {
            'type': 'ir.actions.act_window',
            'views': [(tree_view_id, 'tree'), (form_view_id, 'form')],
            'view_mode': 'tree,form',
            'name': _('Products'),
            'res_model': 'product.product',
            'domain': domain,
            'context': dict(self.env.context, to_date=inventory_date),
        }
        my_action = action


    def action_bad_stock_search(self):

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

        filename = "Bad Stock Wizard"

        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Bad Stock Wizard')


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
        sheet.merge_range(1, 3, 2, 6,"Bad Stock Wizard", format0)
        sheet.merge_range(2, 7, 2, 8,"Date : "+str(datetime.today().strftime('%Y-%m-%d')), format1)

        sheet.set_column(4, 0, 9, without_borders)
        sheet.set_column(4, 9, 19, without_borders)
        sheet.write('A4', 'No', table_header_formate)
        sheet.write('B4', 'Product Code', table_header_formate)
        sheet.write('C4', 'Product Name', table_header_formate)
        sheet.write('D4', 'First Period', table_header_formate)
        sheet.write('E4', 'Ingoing', table_header_formate)
        sheet.write('F4', 'Outgoing', table_header_formate)
        sheet.write('G4', 'Balance', table_header_formate)
        sheet.write('H4', 'First Period Outgoing', table_header_formate)
        sheet.write('I4', 'Avg Of Cost', table_header_formate)
        sheet.write('J4', 'The Cost', table_header_formate)



        row = 4
        seq = 1
        col = 0
        if self.search_by =='product':
            all_stock_move_of_period = self.env['stock.move.line'].search(
                [('date', '>=', self.date_from), ('date', '<=', self.date_to),('product_id','=',self.product_id.id)])
        elif self.search_by =='categ':
            all_stock_move_of_period = self.env['stock.move.line'].search(
                [('date', '>=', self.date_from), ('date', '<=', self.date_to),('product_id.categ_id','in',self.product_categ_ids.ids)])
        elif not self.search_by :
            all_stock_move_of_period = self.env['stock.move.line'].search(
                [('date', '>=', self.date_from), ('date', '<=', self.date_to)])

        all_product_of_this_period = all_stock_move_of_period.mapped('product_id')
        all_from_location_this_period = all_stock_move_of_period.mapped('location_id')
        all_to_location_this_period = all_stock_move_of_period.mapped('location_dest_id')


        if self.location_id:
            all_from_location_this_period = all_from_location_this_period.filtered(lambda l: l.id == self.location_id.id )
            all_to_location_this_period = all_to_location_this_period.filtered(lambda l: l.id == self.location_id.id )


        for rec in all_product_of_this_period:
            product = rec.id
            domain = ([('id', '=', product)])
            my_products = self.env['product.product'].search(domain).with_context(
                dict(self.env.context, to_date=self.date_from))
            first_balance = my_products[0].qty_available
            if self.location_id:
                wared = sum (all_stock_move_of_period.filtered(lambda l: l.product_id.id == rec.id and l.location_dest_id.id ==self.location_id.id ).mapped('qty_done'))
                monsaref = sum (all_stock_move_of_period.filtered(lambda l: l.product_id.id == rec.id and l.location_id.id ==self.location_id.id ).mapped('qty_done'))
            else:
                wared = 0
                monsaref = 0
                for location in all_to_location_this_period :
                    wared += sum (all_stock_move_of_period.filtered(lambda l: l.product_id.id == rec.id and l.location_dest_id.id ==location.id ).mapped('qty_done'))
                for location2 in all_from_location_this_period:
                    monsaref += sum(all_stock_move_of_period.filtered(
                        lambda l: l.product_id.id == rec.id and l.location_id.id == location2.id).mapped(
                        'qty_done'))

            sheet.write(row, col, str(seq) or '', font_size_10)
            sheet.write(row, col + 1, rec.default_code or '', font_size_10)
            sheet.write(row, col + 2, rec.name or '', font_size_10)
            sheet.write(row, col + 3, first_balance or '', font_size_10)
            sheet.write(row, col + 4, wared or '', font_size_10)
            sheet.write(row, col + 5, monsaref or '', font_size_10)
            sheet.write(row, col + 6, rec.qty_available or '', font_size_10)
            sheet.write(row, col + 7, first_balance - monsaref or '', font_size_10)
            sheet.write(row, col + 8, rec.standard_price or '', font_size_10)
            sheet.write(row, col + 9, (first_balance - monsaref) * rec.standard_price or '', font_size_10)

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








# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
import xlsxwriter
from io import BytesIO
import base64
from datetime import datetime


class ExcelReportWizard(models.TransientModel):
    _name = 'stock.card.report.excel'

    excel_file = fields.Binary('Download report Excel', attachment=True, readonly=True)
    file_name = fields.Char('Excel File', size=64)


class StockCardWizard(models.TransientModel):
    _name = 'stock.card.wizard'

    excel_file = fields.Binary('Download report Excel', attachment=True, readonly=True)
    file_name = fields.Char('Excel File', size=64)
    date_from = fields.Date(string="Date From", required=True)
    date_to = fields.Date(string="Date To", required=True)
    location_id = fields.Many2one('stock.location', string="Location", domain=[('usage', '=', 'internal')],
                                  required=True)
    product_id = fields.Many2one('product.product', string="Product", required=True)

    def stock_card_search(self):
        act = self.generate_excel()

        return {

            'type': 'ir.actions.act_window',
            'res_model': 'stock.card.report.excel',
            'res_id': act.id,
            'view_type': 'form',
            'view_mode': 'form',
            'context': self.env.context,
            'target': 'new',

        }

    def write_static_data(self, sheet):
        pass

    def write_file_headers(self, sheet):
        pass

    def generate_excel(self):
        filename = "Stock Card"

        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('data')

        without_borders = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'text_wrap': True,
            'font_size': '11',

        })
        format0 = workbook.add_format({'font_size': 20, 'align': 'center', 'bold': True})
        format1 = workbook.add_format({'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'bold': False, 'border': 1})

        sheet.set_column(3, 3, 30)
        sheet.set_column(3, 5, 20)
        font_size_10 = workbook.add_format(
            {'font_name': 'KacstBook', 'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
             'border': 1})
        table_header_format = workbook.add_format({
            'bold': 1,
            'border': 1,
            'bg_color': '#AAB7B8',
            'font_size': '10',
            'align': 'center',
            'valign': 'vcenter',
            'text_wrap': True
        })
        sheet.merge_range('C4:E5', "موسسة النحام للتجارة", format0)
        # sheet.merge_range(2, 7, 2, 8, "Date : " + str(datetime.today().strftime('%Y-%m-%d')), format1)

        sheet.write('F7', 'اسم المنتج', format1)
        sheet.merge_range('A7:E7', self.product_id.display_name, format1)
        sheet.write('F8', 'المخزن', format1)
        sheet.write('E8', self.location_id.complete_name, format1)
        sheet.write('D8', 'الوحدة', format1)
        sheet.write('C8', self.product_id.uom_id.name, format1)
        # sheet.set_column()
        transfers_to_date = self.env['stock.move.line'].search([('state', '=', 'done'),('product_id', '=', self.product_id.id),
                                                                ('date', '<', self.date_from),
                                                                ('location_dest_id', '=', self.location_id.id)])
        transfers_from_date = self.env['stock.move.line'].search([('state', '=', 'done'),('product_id', '=', self.product_id.id),
                                                                  ('date', '<', self.date_from),
                                                                  ('location_id', '=', self.location_id.id)])
        total_qty_to_date = sum(transfers_to_date.mapped('qty_done'))
        total_qty_from_date = sum(transfers_from_date.mapped('qty_done'))
        start_period_qty = total_qty_to_date - total_qty_from_date
        sheet.merge_range('F9:F10', 'كمية بداية المدة', format1)
        sheet.write('F11', start_period_qty, format1)
        sheet.merge_range('D9:E9', 'الحركة', format1)
        sheet.write('E10', 'وارد', format1)
        sheet.write('D10', 'منصرف', format1)
        sheet.merge_range('C9:C10', 'كمية آخر المدة', format1)

        sheet.write('G15', 'تسلسل', table_header_format)
        sheet.write('F15', 'التاريخ', table_header_format)
        sheet.write('E15', 'الرقم المستندي', table_header_format)
        sheet.write('D15', 'نوع ورقم الفاتورة', table_header_format)
        sheet.write('C15', 'وارد', table_header_format)
        sheet.write('B15', 'منصرف', table_header_format)
        sheet.write('A15', 'الرصيد', table_header_format)

        row = 15
        seq = 1
        col = 6
        transfers = self.env['stock.move.line'].search([('state', '=', 'done'),('product_id', '=', self.product_id.id),
                                                        ('date', '<=', self.date_to),
                                                        ('date', '>=', self.date_from),
                                                        '|',
                                                        ('location_id', '=', self.location_id.id),
                                                        ('location_dest_id', '=', self.location_id.id)])
        income_sum = 0
        outcome_sum = 0
        credit = start_period_qty
        for rec in transfers:
            sheet.write(row, col, seq or '', font_size_10)
            sheet.write(row, col - 1, str(rec.date) or '', font_size_10)
            sheet.write(row, col - 2, rec.reference or '', font_size_10)
            sheet.write(row, col - 3, rec.picking_id.origin or '', font_size_10)
            if self.location_id.id == rec.location_id.id:
                sheet.write(row, col - 4, '', font_size_10)
                sheet.write(row, col - 5, rec.qty_done or '', font_size_10)
                credit -= rec.qty_done
                sheet.write(row, col - 6, credit, font_size_10)
                outcome_sum += rec.qty_done
            elif self.location_id.id == rec.location_dest_id.id:
                sheet.write(row, col - 4, rec.qty_done or '', font_size_10)
                sheet.write(row, col - 5, '', font_size_10)
                credit += rec.qty_done
                sheet.write(row, col - 6, credit, font_size_10)
                income_sum += rec.qty_done
            row += 1
            seq += 1
        sheet.write('E11', income_sum or '', format1)
        sheet.write('D11', outcome_sum or '', format1)
        sheet.write('C11', str(credit) or '', format1)
        workbook.close()
        output.seek(0)

        self.write({'file_name': filename + str(datetime.today().strftime('%Y-%m-%d')) + '.xlsx'})
        self.excel_file = base64.b64encode(output.read())

        context = {
            'file_name': self.file_name,
            'excel_file': self.excel_file,
        }

        act_id = self.env['stock.card.report.excel'].create(context)
        return act_id

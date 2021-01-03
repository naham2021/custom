# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError
import xlsxwriter
from io import BytesIO
import base64
from datetime import datetime




class excelreport(models.TransientModel):
    _name = 'report.excel'

    excel_file = fields.Binary('Dowload report Excel', attachment=True, readonly=True)
    file_name = fields.Char('Excel File', size=64)




class inventorynotinvoicewizard(models.TransientModel):
    _name = 'inventory.not.invoice.wizard'


    excel_file = fields.Binary('Download report Excel', attachment=True, readonly=True)
    file_name = fields.Char('Excel File', size=64)
    type = fields.Selection([('sale','Sale'),('purchase','Purchase')])


    def action_inventory_not_invoice_search(self):
        sale_order_lines = self.env['sale.order.line'].search([('state','in',('sale','done'))])




        act = self.generate_excel(sale_order_lines)

        return {

                'type': 'ir.actions.act_window',
                'res_model': 'report.excel',
                'res_id': act.id,
                'view_type': 'form',
                'view_mode': 'form',
                'context': self.env.context,
                'target': 'new',

            }

    def action_inventory_not_invoice_search_purchase(self):
        purchase_order_lines = self.env['purchase.order.line'].search([('state','in',('purchase','done'))])




        act = self.generate_excel_purchase(purchase_order_lines)

        return {

                'type': 'ir.actions.act_window',
                'res_model': 'report.excel',
                'res_id': act.id,
                'view_type': 'form',
                'view_mode': 'form',
                'context': self.env.context,
                'target': 'new',

            }



    def generate_excel(self, sale_order_lines):

        filename = "Inventory Doesn't Invoiced"

        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Inventory Does Not Invoiced ')


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
        sheet.merge_range(1, 3, 2, 6,"Inventory Doesn't Invoiced", format0)
        sheet.merge_range(2, 7, 2, 8,"Date : "+str(datetime.today().strftime('%Y-%m-%d')), format1)

        sheet.set_column(4, 0, 9, without_borders)
        sheet.set_column(4, 9, 19, without_borders)
        sheet.write('A4', 'No', table_header_formate)
        sheet.write('B4', 'Salesman', table_header_formate)
        sheet.write('C4', 'Value', table_header_formate)
        sheet.write('D4', 'price unit', table_header_formate)
        sheet.write('E4', 'Qty', table_header_formate)
        sheet.write('F4', 'Warehouse', table_header_formate)
        sheet.write('G4', 'Name', table_header_formate)
        sheet.write('H4', 'Customer', table_header_formate)
        sheet.write('I4', ' Date', table_header_formate)
        sheet.write('J4', 'Sale Num', table_header_formate)



        row = 4
        seq = 1
        col = 0
        for rec in sale_order_lines:
            if not (rec.qty_delivered - rec.qty_invoiced == 0 ) and rec.product_id.type != 'service':
                                sheet.write(row, col, str(seq) or '', font_size_10)
                                sheet.write(row, col + 1, rec.order_id.user_id.partner_id.ref or '', font_size_10)
                                sheet.write(row, col + 2, rec.purchase_price or '', font_size_10)
                                sheet.write(row, col + 3, rec.price_unit or '', font_size_10)
                                sheet.write(row, col + 4, rec.qty_delivered-rec.qty_invoiced or '', font_size_10)
                                sheet.write(row, col + 5, rec.order_id.warehouse_id.name or '', font_size_10)
                                sheet.write(row, col + 6, rec.order_id.partner_id.name or '', font_size_10)
                                sheet.write(row, col + 7, rec.order_id.partner_id.ref or '', font_size_10)
                                sheet.write(row, col + 8, str(rec.order_id.date_order) or '', font_size_10)
                                sheet.write(row, col + 9, rec.order_id.name or '', font_size_10)

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


    def generate_excel_purchase(self, purchase_order_lines):

        filename = "Inventory Doesn't Billed"

        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Inventory Does Not Billed ')


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
        sheet.merge_range(1, 3, 2, 6,"Inventory Doesn't Billed", format0)
        sheet.merge_range(2, 7, 2, 8,"Date : "+str(datetime.today().strftime('%Y-%m-%d')), format1)

        sheet.set_column(4, 0, 9, without_borders)
        sheet.set_column(4, 8, 19, without_borders)
        sheet.write('A4', 'No', table_header_formate)
        sheet.write('B4', 'Salesman', table_header_formate)
        sheet.write('C4', 'Price Unit', table_header_formate)
        sheet.write('D4', 'Qty', table_header_formate)
        sheet.write('E4', 'Warehouse', table_header_formate)
        sheet.write('F4', 'Name', table_header_formate)
        sheet.write('G4', 'Customer', table_header_formate)
        sheet.write('H4', ' Date', table_header_formate)
        sheet.write('I4', 'Sale Num', table_header_formate)



        row = 4
        seq = 1
        col = 0
        for rec in purchase_order_lines:
            if not (rec.qty_received - rec.qty_invoiced == 0 ) and rec.product_id.type != 'service':
                                sheet.write(row, col, str(seq) or '', font_size_10)
                                sheet.write(row, col + 1, rec.order_id.user_id.partner_id.ref or '', font_size_10)
                                sheet.write(row, col + 2, rec.price_unit or '', font_size_10)
                                sheet.write(row, col + 3, rec.qty_received-rec.qty_invoiced or '', font_size_10)
                                sheet.write(row, col + 4, rec.order_id.picking_type_id.warehouse_id.name or '', font_size_10)
                                sheet.write(row, col + 5, rec.order_id.partner_id.name or '', font_size_10)
                                sheet.write(row, col + 6, rec.order_id.partner_id.ref or '', font_size_10)
                                sheet.write(row, col + 7, str(rec.order_id.date_approve) or '', font_size_10)
                                sheet.write(row, col + 8, rec.order_id.name or '', font_size_10)

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





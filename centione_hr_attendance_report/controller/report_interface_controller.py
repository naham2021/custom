from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import serialize_exception,content_disposition


class ReportInterfaceController(http.Controller):

    @http.route('/attendance_report', type='http', auth="public")
    @serialize_exception
    def report(self, report_type, group_by=None, date_from=None, date_to=None, filter_by=None, filter_ids=None, **kw):
        print("Hello from controller")
        execute = request.env['report.interface'].context().get(report_type)
        if filter_ids:
            filter_ids = filter_ids.replace('[', '').replace(']', '')
            filter_ids = [int(i) for i in filter_ids.split(',')]
        if execute:
            pdf = execute(group_by=group_by, date_from=date_from, date_to=date_to, filter_by=filter_by, filter_ids=filter_ids)
            pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))]
            return request.make_response(pdf, headers=pdfhttpheaders)

        return "ERROR, NOT FOUND!!"

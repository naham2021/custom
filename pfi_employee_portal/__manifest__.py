# -*- coding: utf-8 -*-
{
    'name': 'PFI Employee Portal Access',
    'version': '1.0',
    'category': 'Human Resources',
    'summary': 'Give Employees Portal Access',
    'description': """
Give Employees Portal Access:
=======================================================

* to be listed
    """,
    'website': 'https://www.centione.com',
    'depends': [ 'hr','odoo_leave_request_portal_employee','odoo_portal_attendance'],
    'data': [
            'views/hr_employee.xml',
            'wizard/employee_portal_wizard.xml',

    ]
}

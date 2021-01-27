# -*- coding: utf-8 -*-
{
    'name': "Portal HR Self Service",

    'summary': """
        Portal HR Self Service
        """,

    'description': """
        Portal HR Self Service
    """,

    'author': "E.Mudathir",
    'website': "http://www.centione.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['centione_hr_self_service','pfi_employee_portal','centione_over_time'],

    # always loaded
    'data': [
        'security/portal_self_service_security.xml',
        'security/ir.model.access.csv',
        'views/templates.xml',
        # 'views/website_portal_excuse.xml',
        'views/website_portal_excuse.xml',
        'views/website_portal_transport.xml',
        'views/website_portal_mission.xml',
        'views/website_portal_loan.xml',
        'views/website_portal_overtime.xml',
        'views/templates.xml',
    ],

}
# -*- coding: utf-8 -*-
{
    'name': "Centione HR Attendance Report",

    'summary': """
        """,

    'description': """
    """,

    'author': "Centione",
    'website': "http://www.centione.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['centione_hr_late_early_absence'],

    # always loaded
    'data': [
        'templates/absence_report.xml',
        'templates/report.xml',
        'wizards/report_interface.xml',
        'security/ir.model.access.csv',
    ],
}
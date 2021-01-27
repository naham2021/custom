# -*- coding: utf-8 -*-
{
    'name': "مؤثرات علي الحضور والانصراف",

    'summary': """""",

    'description': """
       
    """,

    'author': "Centione",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr_payroll','centione_hr_payroll_base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/salary_rules_custom.xml',
        'views/moatherat_attendance.xml',
        'views/late_deductions.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
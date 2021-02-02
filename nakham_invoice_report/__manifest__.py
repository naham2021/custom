# -*- coding: utf-8 -*-
{
    'name': "nakham_invoice_report",
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Accounting Report',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account','nakham_journals_invoices'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views_3.xml',
        'views/views.xml',
        'views/nakham2.xml',
        'views/templates.xml',
    ]
}

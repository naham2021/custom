# -*- coding: utf-8 -*-
{
    'name': "Nakham Invoice Report Inherit",

    # any module necessary for this one to work correctly
    'depends': ['base', 'nakham_invoice_report', 'point_of_sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

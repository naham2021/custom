# -*- coding: utf-8 -*-
{
    'name': "Nakham Category Group By",
    'depends': ['base', 'stock', 'stock_account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

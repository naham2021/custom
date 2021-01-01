# -*- coding: utf-8 -*-
{
    'name': "Nakham Dest Location Domain",

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/stock_picking.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/res_users_inherit.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
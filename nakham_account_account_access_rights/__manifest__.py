# -*- coding: utf-8 -*-
{
    'name': "Nakham Account Account Access Rights",
    'depends': ['base', 'account'],

    # always loaded
    'data': [
        'views/views.xml',
        # 'security/ir.model.access.csv',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

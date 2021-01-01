# -*- coding: utf-8 -*-
{
    'name': "Nakham Analytic Account Access Write",
    'depends': ['base', 'analytic'],

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

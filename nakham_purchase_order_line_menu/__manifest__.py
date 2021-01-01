# -*- coding: utf-8 -*-
{
    'name': "nakham Purchase Order Line Menu",
    'depends': ['base', 'purchase', 'sale'],

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

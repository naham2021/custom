# -*- coding: utf-8 -*-
{
    'name': "Nakham Invoice Line Menu",
    'depends': ['base', 'account', 'stock_landed_costs','nakham_sales_team_rule'],

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

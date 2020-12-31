# -*- coding: utf-8 -*-
{
    'name': "Nakham Accounting Reporting Groups",
    'depends': ['base', 'account_auto_transfer', 'account', 'account_asset', 'account_accountant'],

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

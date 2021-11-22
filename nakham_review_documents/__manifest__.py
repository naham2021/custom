# -*- coding: utf-8 -*-
{
    'name': "nakham_review_documents",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','account','purchase','stock_landed_costs'],

    # always loaded
    'data': [
        'security/security.xml',
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/sale_views.xml',
        'views/account_move_views.xml',
        # 'views/pos_order_views.xml',
        # 'views/pos_session_views.xml',
        # 'views/pos_payment_views.xml',
        'views/purchase_views.xml',
        'views/stock_picking.xml',
        'views/stock_inventory.xml',
        'views/stock_scrap.xml',
        'views/stock_landed_costs.xml',
        'views/account_payment_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

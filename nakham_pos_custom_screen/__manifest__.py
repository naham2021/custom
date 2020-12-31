# -*- coding: utf-8 -*-
{
    'name': "POS Screen Resize & Product List View",

    'summary': """
        POS Screen Resize & Product List View""",

    'description': """
        POS Screen Resize & Product List View
    """,

    'author': "E.Mudathir",
    'website': "https://www.linkedin.com/in/mudathir-ahmed-b97ab3121/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Point of Sale',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['point_of_sale','pos_stock_quantity'],#ks_pos_low_stock_alert

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'qweb': ['static/src/xml/pos.xml'],
   
}
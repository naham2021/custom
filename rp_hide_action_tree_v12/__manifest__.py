#-*- coding:utf-8 -*-
{
    'name': "RP Tree Hide Archive, Delete and Export Option",
    'version': '12.0.1.0.0',
    'description': "Hide archive, delete and export options in tree view",
    'summary': 'This module helps to show export, archive and delete options from tree view based on groups.',
    'author': 'RP Odoo Developer',
    'category': 'Web',
    'license': "OPL-1",
    'depends': ['web'],
    'data': [
        'security/groups.xml',
        'views/assets.xml',
    ],
    'images': [
        'static/description/banner.png',
    ],
    'installable': True,
}

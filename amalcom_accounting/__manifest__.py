# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

{
    'name': "Amalcom customised Accounting",
    'summary': """Amalcom customised Accounting """,
    'description': """
        Amalcom customised Accounting
    """,
    'author': 'Lucidspire.',
    'website': 'http://www.lucidspire.com',
    'category': 'Accounting',
    'version': '1.0',
    'license': 'OPL-1',
    'depends': ['base','account','om_account_followup','om_recurring_payments','payment','om_account_budget'],
    'data': [
        'views/account_move_views.xml',
        'views/menu_hide_views.xml'
        
    ],
    'demo': [
    ],
    'images': [
    ],
    "price": 0.0,
    "currency": "EUR",
    'installable': True,
    'application': True,
    'auto_install': False,
}

# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

{
    'name': "HR Employee Visa",
    'summary': """HR Employee Visa """,
    'description': """
        Manage all employee's visa request for any business or personal trip.
        Behalf of employee, HR department will manage visa process with Government/Visa council.
    """,
    'author': 'Lucidspire.',
    'website': 'http://www.lucidspire.com',
    'category': 'Generic Modules/Human Resources',
    'version': '1.0',
    'license': 'OPL-1',
    'depends': ['base','mail','hr','product','contacts','web'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequences.xml',
        'security/ir_rule.xml',

        'views/configurations/employment_duration_views.xml',
        'views/configurations/letter_print_type_views.xml',
        'views/configurations/res_partner_phonecode_views.xml',
        'views/configurations/salary_structure_views.xml',
        'views/configurations/service_pricing_views.xml',
        'views/configurations/visa_ref_documents_views.xml',
        
        'views/hr_employee_views.xml',
        'views/res_bank_views.xml',
        'views/res_users_views.xml',
        
        'views/employment_visa_views.xml',
        'views/local_transfer_views.xml',
        'views/smart_buttons_views.xml',
        
        'views/res_partner_views.xml',

        'views/service_enquiry_views.xml',
        
        
        
        
        'views/menu.xml',
    ],
    'demo': [
        # 'demo/visa_demo.xml',
    ],
    'images': [
        'static/description/main_screen.jpg'
    ],
    "price": 0.0,
    "currency": "EUR",
    'installable': True,
    'application': True,
    'auto_install': False,
}

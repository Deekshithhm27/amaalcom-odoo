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
    'depends': ['base','mail','hr','product','contacts','hr_skills'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequences.xml',
        # uncomment later
        'security/ir_rule.xml',
        'views/salary_structure_views.xml',
        'views/visa_candidate_views.xml',
        'views/employment_duration_views.xml',
        'views/visa_candidate_documents_views.xml',
        'views/service_request_type_views.xml',
        # 'views/service_request_approval_views.xml',
        'views/service_request_views.xml',
        'views/smart_buttons_views.xml',
        'views/res_partner_views.xml',
        'views/res_bank_views.xml',
        'views/menu.xml',

        # 'report/visit_visa.xml',
        # 'report/embassy_visit_visa.xml',
        # 'report/business_visa.xml',
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

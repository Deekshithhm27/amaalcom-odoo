# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime
from dateutil import relativedelta as rdelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class ResPartner(models.Model):
    _inherit = 'res.partner'

    client_code = fields.Char(string="Client Code")
    is_client = fields.Boolean(string='Is a client', default=False,
        help="Check if the contact is a client",store=True,compute="_check_type_of_partner")

    # Overrided fields
    vat = fields.Char(string='VAT', index=True, help="The Tax Identification Number. Complete it if the contact is subjected to government taxes. Used in some legal statements.")

    @api.onchange('user_ids')
    def update_parent_id(self):
        print("-------------------")
        for line in self:
            if line.user_ids:
                for user in user_ids:
                    line.parent_id = user.partner_company_id

    @api.depends('user_ids')
    def _check_type_of_partner(self):
        for line in self:
            if line.user_ids:
                for user in line.user_ids:
                    if user.user_type == 'external':
                        line.is_client = True
                        line.parent_id = user.partner_company_id
                    else:
                        line.is_client = False
                        line.parent_id = user.partner_company_id
            else:
                line.is_client = False




    employees_count = fields.Integer(compute='_compute_employees_count')
    employment_visa_count = fields.Integer(compute='_compute_employment_visa_count')

    company_spoc_id = fields.Many2one('hr.employee',string="Accounts Manager",tracking=True)



    def _compute_employees_count(self):
        for line in self:
            employee_id = self.env['hr.employee'].search([('client_id', '=', line.id)])
            line.employees_count = len(employee_id)

    def _compute_employment_visa_count(self):
        for line in self:
            emp_visa_id = self.env['employment.visa'].search([('client_id', '=', line.id)])
            line.employment_visa_count = len(emp_visa_id)

    
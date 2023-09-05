# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class ServicePricing(models.Model):
    _name = 'service.pricing'
    _order = 'id asc'
    _inherit = ['mail.thread']
    _rec_name = 'name'
    _description = "Service Pricing"

    name = fields.Char(string="Type",tracking=True,store=True,compute='update_name')
    active = fields.Boolean('Active', default=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.user.company_id)
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)

    service_request = fields.Selection([('lt_request','Local Transfer'),('ev_request','Employment Visa')],string="Service Request",default='lt_request',tracking=True)
    ev_service_request_type = fields.Selection([('new_ev','Issuance of New EV'),
        ('sec','SEC Letter'),('hr_card','Issuance for HR card'),
        ('ins_class_upgrade','Medical health insurance Class Upgrade'),
        ('iqama_no_generation','Iqama No generation'),('iqama_card_req','New Physical Iqama Card Request'),
        ('qiwa','Qiwa Contract'),('gosi','GOSI Update'),('iqama_renewal','Iqama Renewal'),('exit_reentry_issuance','Exit Rentry issuance'),
        ('prof_change_qiwa','Profession change Request In qiwa'),('salary_certificate','Salary certificate'),
        ('bank_letter','Bank letter'),('vehicle_lease','Letter for Vehicle Lease'),
        ('apartment_lease','Letter for Apartment Lease'),('istiqdam_form','Istiqdam Form(Family Visa Letter)'),
        ('family_visa_letter','Family Visa Letter'),('employment_contract','Employment contract'),
        ('cultural_letter','Cultural Letter/Bonafide Letter'),
        ('family_visit_visa','Family Visit Visa'),
        ('emp_secondment_or_cub_contra_ltr','Employee secondment / Subcontract letter'),
        ('car_loan','Car Loan Letter'),('bank_loan','Bank Loan Letter'),('rental_agreement','Rental Agreement Letter'),
        ('exception_letter','Exception Letter'),('attestation_waiver_letter','Attestation Waiver Letter'),
        ('embassy_letter','Embassy Letters- as Per Respective Embassy requirement'),('istiqdam_letter','Istiqdam Letter'),
        ('sce_letter','SCE Letter'),('bilingual_salary_certificate','Bilingual Salary Certificate'),('contract_letter','Contract Letter'),
        ('bank_account_opening_letter','Bank account Opening Letter'),('bank_limit_upgrading_letter','Bank Limit upgrading Letter'),
        ('final_exit_issuance','Final exit Issuance'),
        ('dependent_transfer_query','Dependent Transfer Query'),('soa','Statement of account till date'),('general_query','General Query')],string="Requests")
    lt_service_request_type = fields.Selection([('hr_card','Issuance for HR card'),
        ('ins_class_upgrade','Medical health insurance Class Upgrade'),
        ('iqama_no_generation','Iqama No generation'),('iqama_card_req','New Physical Iqama Card Request'),
        ('qiwa','Qiwa Contract'),('gosi','GOSI Update'),('iqama_renewal','Iqama Renewal'),('exit_reentry_issuance','Exit Rentry issuance'),
        ('prof_change_qiwa','Profession change Request In qiwa'),('salary_certificate','Salary certificate'),
        ('bank_letter','Bank letter'),('vehicle_lease','Letter for Vehicle Lease'),('apartment_lease','Letter for Apartment Lease'),
        ('istiqdam_form','Istiqdam Form(Family Visa Letter)'),('family_visa_letter','Family Visa Letter'),('employment_contract','Employment contract'),
        ('cultural_letter','Cultural Letter/Bonafide Letter'),
        ('family_visit_visa','Family Visit Visa'),
        ('emp_secondment_or_cub_contra_ltr','Employee secondment / Subcontract letter'),
        ('car_loan','Car Loan Letter'),('bank_loan','Bank Loan Letter'),('rental_agreement','Rental Agreement Letter'),
        ('exception_letter','Exception Letter'),('attestation_waiver_letter','Attestation Waiver Letter'),
        ('embassy_letter','Embassy Letters- as Per Respective Embassy requirement'),('istiqdam_letter','Istiqdam Letter'),
        ('sce_letter','SCE Letter'),('bilingual_salary_certificate','Bilingual Salary Certificate'),('contract_letter','Contract Letter'),
        ('bank_account_opening_letter','Bank account Opening Letter'),('bank_limit_upgrading_letter','Bank Limit upgrading Letter'),
        ('final_exit_issuance','Final exit Issuance'),
        ('dependent_transfer_query','Dependent Transfer Query'),('soa','Statement of account till date'),('general_query','General Query')],string="Requests")

    pricing_line_ids = fields.One2many('service.pricing.line','pricing_id',string="Pricing Line",copy=True)

    @api.depends('service_request', 'ev_service_request_type', 'lt_service_request_type')
    def update_name(self):
        for visa in self:
            service_request = dict(self._fields['service_request'].selection).get(visa.service_request)
            if visa.ev_service_request_type and visa.service_request == 'ev_request':
                ev_service_request_type = dict(self._fields['ev_service_request_type'].selection).get(visa.ev_service_request_type)
                visa.name = ''.join([ ev_service_request_type or '', ' (','EV', ')'])
            else:
                lt_service_request_type = dict(self._fields['lt_service_request_type'].selection).get(visa.lt_service_request_type)
                visa.name = ''.join([lt_service_request_type or '', ' (', 'LT', ')'])


    @api.depends('service_request', 'ev_service_request_type', 'lt_service_request_type')
    def name_get(self):
        """
        to use retrieving the name, combination of `service request, 
        Ev service request type and Lt service request type`
        """
        result = []
        for visa in self:
            service_request = dict(self._fields['service_request'].selection).get(visa.service_request)
            if visa.ev_service_request_type and visa.service_request == 'ev_request':
                ev_service_request_type = dict(self._fields['ev_service_request_type'].selection).get(visa.ev_service_request_type)
                name = ''.join([ev_service_request_type or '', ' (','EV', ')'])
            else:
                lt_service_request_type = dict(self._fields['lt_service_request_type'].selection).get(visa.lt_service_request_type)
                name = ''.join([lt_service_request_type or '', ' (', 'LT', ')'])
            result.append((visa.id, name))
        return result

    @api.onchange('service_request')
    def update_service_request(self):
        for line in self:
            if line.service_request == 'ev_request':
                line.lt_service_request_type = False
            if line.service_request == 'lt_request':
                line.ev_service_request_type = False




class ServicePricingLine(models.Model):
    _name = 'service.pricing.line'
    _order = 'id asc'
    _inherit = ['mail.thread']
    _rec_name = 'duration_id'
    _description = "Service Pricing Line"


    pricing_id = fields.Many2one('service.pricing',string="Service Pricing")

    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.user.company_id)
    currency_id = fields.Many2one('res.currency', string='Currency', store=True, readonly=False,
        related="company_id.currency_id",help="The payment's currency.")

    duration_id = fields.Many2one('employment.duration',string="Duration")
    amount = fields.Monetary(string="Amount")
    remarks = fields.Text(string="Remarks")


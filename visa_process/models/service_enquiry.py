# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError,UserError
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class ServiceEnquiry(models.Model):
    _name = 'service.enquiry'
    _order = 'id desc'
    _inherit = ['mail.thread']
    _rec_name = 'name'
    _description = "Service Enquiry"

    name = fields.Char(string="Enquiry No")
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.user.company_id)
    client_id = fields.Many2one('res.partner',string="Client",default=lambda self: self.env.user.partner_id)
    approver_id = fields.Many2one('hr.employee',string="Approver")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted','Ticket Submitted'),
        ('payment_initiation','Payment Initiation'),
        ('payment_done','Payment Confirmation'),
        ('done', 'Done'),('refuse','Refuse'),('cancel','Cancel')], string='State',default="draft",copy=False,tracking=True)
    service_request = fields.Selection([('lt_request','Local Transfer'),('ev_request','Employment Visa')],string="Service Request",default='lt_request',tracking=True)
    ev_service_request_type = fields.Selection([('issuance_of_new_ev','Issuance of New EV'),
        ('sec_letter','SEC Letter'),('issuance_of_hr_card','Issuance for HR card'),
        ('medical_health_insurance_class_upgrade','Medical health insurance Class Upgrade'),
        ('iqama_no_generation','Iqama No generation'),('new_physical_iqama_card_request','New Physical Iqama Card Request'),
        ('qiwa_contract','Qiwa Contract'),('gosi_update','GOSI Update'),('iqama_renewal','Iqama Renewal'),('exit_reentry_issuance','Exit Rentry issuance'),
        ('profession_change_request_in_qiwa','Profession change Request In qiwa'),('salary_certificate','Salary certificate'),
        ('bank_letter','Bank letter'),('letter_for_vehicle_lease','Letter for Vehicle Lease'),
        ('letter_for_apartment_lease','Letter for Apartment Lease'),('istiqdam_form','Istiqdam Form(Family Visa Letter)'),
        ('family_visa_letter','Family Visa Letter'),('employment_contract','Employment contract'),
        ('cultural_letter','Cultural Letter/Bonafide Letter'),
        ('family_visit_visa','Family Visit Visa'),
        ('emp_secondment_or_cub_contra_ltr','Employee secondment / Subcontract letter'),
        ('car_loan_letter','Car Loan Letter'),('bank_loan_letter','Bank Loan Letter'),('rental_agreement_letter','Rental Agreement Letter'),
        ('exception_letter','Exception Letter'),('attestation_waiver_letter','Attestation Waiver Letter'),
        ('embassy_letter','Embassy Letters- as Per Respective Embassy requirement'),('istiqdam_letter','Istiqdam Letter'),
        ('sce_letter','SCE Letter'),('bilingual_salary_certificate','Bilingual Salary Certificate'),('contract_letter','Contract Letter'),
        ('bank_account_opening_letter','Bank account Opening Letter'),('bank_limit_upgrading_letter','Bank Limit upgrading Letter'),
        ('final_exit_issuance','Final exit Issuance'),
        ('dependent_transfer_query','Dependent Transfer Query'),('soa','Statement of account till date'),('general_query','General Query')],string="Requests")
    lt_service_request_type = fields.Selection([('issuance_of_hr_card','Issuance for HR card'),
        ('medical_health_insurance_class_upgrade','Medical health insurance Class Upgrade'),
        ('iqama_no_generation','Iqama No generation'),('new_physical_iqama_card_request','New Physical Iqama Card Request'),
        ('qiwa_contract','Qiwa Contract'),('gosi_update','GOSI Update'),('iqama_renewal','Iqama Renewal'),('exit_reentry_issuance','Exit Rentry issuance'),
        ('profession_change_request_in_qiwa','Profession change Request In qiwa'),('salary_certificate','Salary certificate'),
        ('bank_letter','Bank letter'),('letter_for_vehicle_lease','Letter for Vehicle Lease'),('letter_for_apartment_lease','Letter for Apartment Lease'),
        ('istiqdam_form','Istiqdam Form(Family Visa Letter)'),('family_visa_letter','Family Visa Letter'),('employment_contract','Employment contract'),
        ('cultural_letter','Cultural Letter/Bonafide Letter'),
        ('family_visit_visa','Family Visit Visa'),
        ('emp_secondment_or_cub_contra_ltr','Employee secondment / Subcontract letter'),
        ('car_loan_letter','Car Loan Letter'),('bank_loan_letter','Bank Loan Letter'),('rental_agreement_letter','Rental Agreement Letter'),
        ('exception_letter','Exception Letter'),('attestation_waiver_letter','Attestation Waiver Letter'),
        ('embassy_letter','Embassy Letters- as Per Respective Embassy requirement'),('istiqdam_letter','Istiqdam Letter'),
        ('sce_letter','SCE Letter'),('bilingual_salary_certificate','Bilingual Salary Certificate'),('contract_letter','Contract Letter'),
        ('bank_account_opening_letter','Bank account Opening Letter'),('bank_limit_upgrading_letter','Bank Limit upgrading Letter'),
        ('final_exit_issuance','Final exit Issuance'),
        ('dependent_transfer_query','Dependent Transfer Query'),('soa','Statement of account till date'),('general_query','General Query')],string="Requests")
    candidate_id = fields.Many2one('visa.candidate',string="Candidate",store=True,tracking=True)
    emp_visa_id = fields.Many2one('employment.visa',string="Service Id",tracking=True)

    @api.onchange('emp_visa_id')
    def update_candidate_id(self):
        for line in self:
            line.candidate_id = line.emp_visa_id.candidate_id



    # LT Fields
    confirmation_on_fees_paid = fields.Binary(string="Confirmation on fees paid LTI")
    bank_id = fields.Many2one('res.bank',string="Bank")
    purpose = fields.Text(string="Purpose?")
    letter_print_type_id = fields.Many2many('letter.print.type',string="Type")
    draft_if_any = fields.Binary(string="Draft if any")
    coc_certification = fields.Selection([('yes','Yes'),('no','No')],string="COC Certification")
    re_entry_issuance = fields.Selection([('single','Single'),('multiple','Multiple')],string="Re-entry issuance")
    from_date = fields.Date(string="From Date")
    valid_reason = fields.Text(string="Valid reason to be stated")
    any_credit_note = fields.Text(string="Any credit note to be issued with reason")
    
    insurance_availability = fields.Selection([('yes','Yes'),('no','No')],string="Medical Insurance")
    medical_doc = fields.Binary(string="Medical Doc")

    upload_hr_card = fields.Binary(string="HR Card Document")
    upload_payment_doc = fields.Binary(string="Payment Confirmation Document")
    residance_doc = fields.Binary(string="Residance Permit Document")
    muqeem_print_doc = fields.Binary(string="Muqeem Print Document")

    upload_upgrade_insurance_doc = fields.Binary(string="Confirmation of Insurance upgarde Document")
    request_date = fields.Datetime(string="Request Date",default=fields.Datetime.now)

    upload_iqama_card = fields.Binary(string="Upload Iqama Card")
    upload_iqama_card_doc = fields.Binary(string="Upload Iqama Card")
    upload_iqama_card_no_doc = fields.Binary(string="Upload Iqama Card")
    upload_qiwa_contract_doc = fields.Binary(string="Upload Qiwa Contract")
    upload_gosi_update_doc = fields.Binary(string="Upload GOSI Update")
    profession_change_doc = fields.Binary(string="Profession Change Req. Doc")
    profession_change_final_doc = fields.Binary(string="Profession Change Req. Doc")
    upload_salary_certificate_doc = fields.Binary(string="Salary Certificate")
    upload_bank_letter_doc = fields.Binary(string="Bank Letter")
    upload_letter_for_vehicle_lease_doc = fields.Binary(string="Letter for Vehicle lease")
    upload_letter_for_apartment_lease_doc = fields.Binary(string="Letter for Apartment lease")
    upload_family_visa_letter_doc = fields.Binary(string="Family Visa Letter")
    upload_visit_visa_app_doc = fields.Binary(string="Upload Visit Visa application")
    upload_family_visit_visa_doc = fields.Binary(string="Family Visit Visa Doc")
    upload_employment_contract_doc = fields.Binary(string="Employment Contract")
    upload_cultural_letter_doc = fields.Binary(string="Cultural Letter")
    draft_istiqdam = fields.Binary(string="Draft Istiqdam",compute="auto_fill_istiqdam_form",store=True)
    updated_istiqdam_form_doc = fields.Binary(string="Updated Istiqdam Form")
    upload_istiqdam_form_doc = fields.Binary(string="Upload Istiqdam Form")
    upload_confirmation_of_exit_reentry = fields.Binary(string="Upload Confirmation of Exit re-entry")
    upload_exit_reentry_visa = fields.Binary(string="Exit Re-entry Visa")
    upload_final_exit_issuance_doc = fields.Binary(string="Final Exit issuance doc")
    upload_soa_doc = fields.Binary(string="SOA Doc")
    upload_emp_secondment_or_cub_contra_ltr_doc = fields.Binary(string="Employee secondment / Subcontract Document")
    upload_car_loan_letter_doc = fields.Binary(string="Car Loan Document")
    upload_bank_loan_letter_doc = fields.Binary(string="Bank Loan Document")
    upload_rental_agreement_letter_doc = fields.Binary(string="Rental Agreement Document")
    upload_exception_letter_doc = fields.Binary(string="Exception Document")
    upload_attestation_waiver_letter_doc = fields.Binary(string="Attestation Waiver Document")
    upload_embassy_letter_doc = fields.Binary(string="Embassy Letter")
    upload_istiqdam_letter_doc = fields.Binary(string="Istiqdam Letter")
    upload_sce_letter_doc = fields.Binary(string="SCE Letter")
    upload_bilingual_salary_certificate_doc = fields.Binary(string="Bilingual Salary Certificate")
    upload_contract_letter_doc = fields.Binary(string="Contract Letter")
    upload_bank_account_opening_letter_doc = fields.Binary(string="Bank account Opening Letter")
    upload_bank_limit_upgrading_letter_doc = fields.Binary(string="Bank Limit upgrading Letter")

    
    reason_for_loss_of_iqama = fields.Text(string="Reason for loss of Iqama")
    letter_from_police_station = fields.Binary(string="Letter from the police station of the lost iqama")
    note = fields.Text(string="Note",default="Note: Cost 1000 sar, invoice not available")
    visit_visa_note = fields.Text(string="Note",default="Note: Document will be Attested by COC ")
    date_from = fields.Date(string="From Date")
    date_to = fields.Date(string="To Date")


    # EV Fields

    visa_country_id = fields.Many2one('res.country',string="Visa issuing country")
    visa_state_id = fields.Many2one('res.country.state',string="Visa issuing city",domain="[('country_id', '=', visa_country_id)]")
    visa_religion = fields.Selection([('muslim','Muslim'),('non_muslim','Non-Muslim'),('others','Others')],string="Visa Religion")
    no_of_visa = fields.Integer(string="No of Visa")
    profession = fields.Char(string="Profession")
    agency_allocation = fields.Text(string="Allocation of Agency (E wakala)")
    coc_for_ewakala = fields.Boolean(string="COC for Ewakala",compute="update_coc_for_ewakala",store=True)

    @api.depends('agency_allocation')
    def update_coc_for_ewakala(self):
        for line in self:
            if line.agency_allocation:
                line.coc_for_ewakala = True
            else:
                line.coc_for_ewakala = False

    upload_issuance_doc = fields.Binary(string="Upload Issuance of Visa Document")
    upload_enjaz_doc = fields.Binary(string="Enjaz Document")
    upload_sec_letter_doc = fields.Binary(string="SEC Letter")

    visa_document = fields.Binary(string="Visa Document")
    chamber = fields.Selection([('yes','Yes'),('no','No')],string="Chamber")
    mofa_draft = fields.Binary(string="Draft")
    mofa_reason = fields.Text(string="Reason for issuing the letter")
    sec_draft = fields.Binary(string="Draft")
    coc = fields.Selection([('yes','Yes'),('no','No')],string="COC")
    sec_upload = fields.Binary(string="Document Upload")
    cost_difference = fields.Selection([('aamalcom','Aamalcom'),('lti','LTI')],string="Cost Difference")





    # Common fields
    employment_duration = fields.Many2one('employment.duration',string="Duration",tracking=True)
    exit_type = fields.Selection([('single','Single'),('multiple','Multiple')],string="Type")

    fees_to_be_paid = fields.Selection([('aamalcom','Aamalcom'),('client','Client')],string="Fees to be paid by")
    fees_to_be_paid_by = fields.Selection([('aamalcom','Aamalcom'),('client','Client'),('candidate','Candidate')],string="Fees to be paid by")
    to_be_issued_date = fields.Date(string="To be issued from")

    current_insurance_class = fields.Selection([('class_vip+','VIP+'),('class_vip','VIP'),('class_a','A'),('class_b','B'),('class_c','C'),('class_e','E')],string="Current Insurance Class")
    class_to_be_changed = fields.Selection([('class_vip+','VIP+'),('class_vip','VIP'),('class_a','A'),('class_b','B'),('class_c','C'),('class_e','E')],string="Class to be changed to!")
    duration_limit = fields.Selection([('30','30'),('60','60'),('90','90'),('120','120'),('150','150'),('180','180'),('210','210'),('240','240'),('270','270'),('300','300'),('330','330'),('360','360')],string="Duration")


    insurance_class = fields.Selection([('class_vip+','VIP+'),('class_vip','VIP'),('class_a','A'),('class_b','B'),('class_c','C'),('class_e','E')],string="Current Insurance Class")

    document_upload = fields.Binary(string="Document Upload")
    logical_reason = fields.Text(string="Logical Reason to be stated")
    border_id_doc = fields.Binary(string="Upload Iqama /Passport with border ID")
    cost_to_be_borne_by = fields.Selection([('aamalcom','Aamalcom'),('client','Client')],string="Cost To be borne by")
    iqama_upload = fields.Binary(string="Iqama Upload")
    profession_change = fields.Char(string="Profession change to")
    soa_date = fields.Date(string="Duration")
    duration = fields.Char(string="Duration")


    # EV fields
    dob = fields.Date(string="DOB",tracking=True)
    contact_no = fields.Char(string="Contact # in the country",tracking=True)
    current_contact = fields.Char(string="Current Contact # (if Outside the country) *",tracking=True)
    email = fields.Char(string="Email Id *",tracking=True)
    nationality_id = fields.Many2one('res.country',string="Nationality",tracking=True)
    phone_code_id = fields.Many2one('res.partner.phonecode',string="Phone code")
    current_phone_code_id = fields.Many2one('res.partner.phonecode',string="Phone code")

    marital = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('cohabitant', 'Legal Cohabitant'),
        ('widower', 'Widower'),
        ('divorced', 'Divorced')
    ], string='Marital Status', groups="hr.group_hr_user", default='single', tracking=True)
    # Employment details
    designation = fields.Char(string="Designation on Offer Letter",tracking=True)
    doj = fields.Date(string="Projected Date of Joining",tracking=True)
    
    probation_term = fields.Char(string="Probation Term",tracking=True)
    notice_period = fields.Char(string="Notice Period",tracking=True)
    working_days = fields.Char(string="Working Days *")
    working_hours = fields.Char(string="Working Hours *")
    annual_vacation = fields.Char(string="Annual Vacation *")
    weekly_off_days = fields.Char(string="Weekly Off (No. Of Days)",tracking=True)

    # # Documents
    # document_line_ids = fields.One2many('candidate.documents.line','service_request_id',string="Documents")
    signed_offer_letter = fields.Binary(string="Signed Offer letter/should be attached *")
    passport_copy = fields.Binary(string="Passport copy *")
    border_copy = fields.Binary(string="Border Id *")
    attested_degree = fields.Binary(string="Attested Degree copy *")
    attested_visa_page = fields.Binary(string="Attested visa page *")
    bank_iban_letter = fields.Binary(string="Bank Iban Letter *")
    certificate_1 = fields.Binary(string="Certificates *")
    certificate_2 = fields.Binary(string="Certificates")
    other_doc_1 = fields.Binary(string="Others")
    other_doc_2 = fields.Binary(string="Others")
    other_doc_3 = fields.Binary(string="Others")
    other_doc_4 = fields.Binary(string="Others")
    

    salary_line_ids = fields.One2many('salary.line', 'ev_enq_visa_id', string="Salary Structure")
    @api.model
    def default_get(self,fields):
        res = super(ServiceEnquiry,self).default_get(fields)
        salary_lines = [(5,0,0)]
        salary_ids = self.env['salary.structure'].search([])
        for sal in salary_ids:
            line = (0,0,{
                'name':sal.id
                })
            salary_lines.append(line)
        res.update({
            'salary_line_ids':salary_lines
            })
        return res

    # Profession Details
    visa_profession = fields.Char(string="Visa Profession *")
    
    visa_nationality_id = fields.Many2one('res.country',string="Visa Nationality *")
    visa_stamping_city_id = fields.Char(string="Visa Stamping City *")
    visa_enjaz = fields.Char(string="Visa Enjaz Details *")
    no_of_visa = fields.Integer(string="No of Visa *")
    visa_fees = fields.Selection([('aamalcom','Aamalcom'),('lti','LTI')],string="Visa Fees")
    visa_gender = fields.Selection([('male','Male'),('female','Female'),('others','Others')],string="Visa Gender *")
    qualification = fields.Char(string="Education Qualification *")

    iqama_designation = fields.Char(string="Designation on Iqama (exact)")
    attested_from_saudi_cultural = fields.Selection([('yes','Yes'),('no','No')],string="Degree attested from saudi cultural")
    
    work_location_id = fields.Many2one('hr.work.location',string="Work Location",tracking=True)

    # Air Fare
    air_fare_for = fields.Selection([('self','Self'),('family','Family')],string="Air Fare for?")
    air_fare_frequency = fields.Char(string="Air Fare Frequency")

    # Medical Insurance
    medical_insurance_for = fields.Selection([('self','Self'),('family','Family')],string="Medical Insurance For?")
    
    dependent_document_ids = fields.One2many('dependent.documents','ev_enq_dependent_document_id',string="Dependent Documents")
    


    # LT fields

    # common fields

    

    request_note = fields.Text(string="Request Query")  

    # LT Issuance of HR Card and Iqama renewal start

    def action_submit(self):
        for line in self:
            line.state = 'submitted'
            self.approver_id = self.client_id.company_spoc_id.id 
            self._add_followers()

    def action_require_payment_confirmation(self):
        for line in self:
            line.state = 'payment_initiation'

    def action_submit_payment_confirmation(self):
        for line in self:
            line.state = 'payment_done'

    

    # LT Issuance of HR Card and Iqama Renewal end



    # LT Medical Health Insurance Upload start

    def action_submit_initiate(self):
        for line in self:
            line.state = 'submitted'

    def action_process_complete(self):
        for line in self:
            line.state = 'done'

    

    # LT Medical Health Insurance Upload end

    @api.onchange('service_request')
    def update_service_request(self):
        for line in self:
            if line.state == 'draft':
                if line.service_request == 'ev_request':
                    line.lt_service_request_type = False
                if line.service_request == 'lt_request':
                    line.ev_service_request_type = False

    @api.depends('lt_service_request_type','ev_service_request_type')
    def auto_fill_istiqdam_form(self):
        for line in self:
            if line.lt_service_request_type == 'istiqdam_form' or line.ev_service_request_type == 'istiqdam_form':
                istiqdam_id = self.env['visa.ref.documents'].search([('is_istiqdam_doc','=',True)],limit=1)
                line.draft_istiqdam = istiqdam_id.istiqdam_doc
            else:
                line.draft_istiqdam = False

    def action_confirm(self):
        for line in self:
            line.state = 'done'

    def action_refuse(self):
        for line in self:
            line.state = 'refuse'

    def action_cancel(self):
        for line in self:
            line.state = 'cancel'

    # New Physical Iqama Card Request(cost 1,000sar) start

    def action_iqama_submit(self):
        for line in self:
            line.state = 'submitted'

    def action_iqama_payment_received_confirmation(self):
        for line in self:
            line.state = 'payment_done'

    def action_iqama_process_complete(self):
        for line in self:
            line.state = 'done'

    # New Physical Iqama Card Request(cost 1,000sar) end

 
    # Issuance of New EV start
    def action_submit_issuance_of_new_ev(self):
        for line in self:
            line.state = 'submitted'

    def action_issuance_of_new_ev_process_complete(self):
        for line in self:
            line.state='done'

    # Issuance of New EV end



    @api.model_create_multi
    def create(self,vals_list):
        for vals in vals_list:
            vals['name'] = self.env['ir.sequence'].next_by_code('service.enquiry')
        res = super(ServiceEnquiry,self).create(vals_list)
        return res

    def _add_followers(self):
        """
            Add Approver as followers
        """
        partner_ids = []
        if self.approver_id:
            partner_ids.append(self.approver_id.user_id.partner_id.id)
        self.message_subscribe(partner_ids=partner_ids)


    doc_uploaded = fields.Boolean(string="Document uploaded",default=False)
    @api.onchange('upload_upgrade_insurance_doc','upload_iqama_card_no_doc','upload_iqama_card_doc','upload_qiwa_contract_doc',
        'upload_gosi_update_doc','upload_hr_card','upload_confirmation_of_exit_reentry','upload_exit_reentry_visa','profession_change_doc',
        'upload_payment_doc','profession_change_final_doc','upload_salary_certificate_doc','upload_bank_letter_doc','upload_letter_for_vehicle_lease_doc',
        'upload_letter_for_apartment_lease_doc','upload_istiqdam_form_doc','upload_family_visa_letter_doc','upload_employment_contract_doc',
        'upload_cultural_letter_doc','upload_family_visit_visa_doc',
        'upload_emp_secondment_or_cub_contra_ltr_doc','upload_car_loan_letter_doc','upload_bank_loan_letter_doc','upload_rental_agreement_letter_doc',
        'upload_exception_letter_doc','upload_attestation_waiver_letter_doc','upload_embassy_letter_doc','upload_istiqdam_letter_doc','upload_sce_letter_doc',
        'upload_bilingual_salary_certificate_doc','upload_contract_letter_doc','upload_bank_account_opening_letter_doc','upload_bank_limit_upgrading_letter_doc','upload_final_exit_issuance_doc','upload_soa_doc',
        'upload_sec_letter_doc')
    def document_uploaded(self):
        for line in self:
            if line.upload_upgrade_insurance_doc or line.upload_iqama_card_no_doc or line.upload_iqama_card_doc or line.upload_qiwa_contract_doc or \
            line.upload_gosi_update_doc or line.upload_hr_card or line.profession_change_doc or line.upload_payment_doc or line.profession_change_final_doc or \
            line.upload_salary_certificate_doc or line.upload_bank_letter_doc or line.upload_letter_for_vehicle_lease_doc or line.upload_letter_for_apartment_lease_doc or \
            line.upload_istiqdam_form_doc or line.upload_family_visa_letter_doc or line.upload_employment_contract_doc or line.upload_cultural_letter_doc or \
            line.upload_family_visit_visa_doc or \
            line.upload_emp_secondment_or_cub_contra_ltr_doc or line.upload_car_loan_letter_doc or line.upload_bank_loan_letter_doc or line.upload_rental_agreement_letter_doc or \
            line.upload_exception_letter_doc or line.upload_attestation_waiver_letter_doc or line.upload_embassy_letter_doc or line.upload_istiqdam_letter_doc or line.upload_sce_letter_doc or \
            line.upload_bilingual_salary_certificate_doc or line.upload_contract_letter_doc or line.upload_bank_account_opening_letter_doc or line.upload_bank_limit_upgrading_letter_doc or \
            line.upload_final_exit_issuance_doc or line.upload_soa_doc or line.upload_sec_letter_doc:
                line.doc_uploaded = True
            elif line.upload_confirmation_of_exit_reentry and line.upload_exit_reentry_visa:
                line.doc_uploaded = True
            else:
                line.doc_uploaded = False

    @api.onchange('ev_service_request_type','lt_service_request_type')
    def update_doc_updated(self):
        for line in self:
            line.doc_uploaded = False
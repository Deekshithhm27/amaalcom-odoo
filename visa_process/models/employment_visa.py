# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError,UserError
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class EmploymentVisa(models.Model):
    _name = 'employment.visa'
    _order = 'id desc'
    _inherit = ['mail.thread']
    _rec_name = 'name'
    _description = "EV Request"

    
    name = fields.Char(string="Sequence",help="The Unique Sequence no", readonly=True, default='/')
    candidate_id = fields.Many2one('visa.candidate',string="Candidate",tracking=True,required=True)
    dob = fields.Date(string="DOB",tracking=True)
    contact_no = fields.Char(string="Contact # in the country",tracking=True)
    current_contact = fields.Char(string="Current Contact # (if Outside the country) *",tracking=True)
    email = fields.Char(string="Email Id *",tracking=True)
    nationality_id = fields.Many2one('res.country',string="Nationality",tracking=True)
    phone_code_id = fields.Char(string="Phone code",compute="fetch_phone_code")

    @api.depends('nationality_id')
    def fetch_phone_code(self):
        for line in self:
            phone_id = self.env['res.partner.phonecode'].search([('country_id','=',line.nationality_id.id)])
            if phone_id:
                for lines in phone_id:
                    line.phone_code_id = lines.name
            else:
                line.phone_code_id = False
    marital = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('cohabitant', 'Legal Cohabitant'),
        ('widower', 'Widower'),
        ('divorced', 'Divorced')
    ], string='Marital Status', groups="hr.group_hr_user", default='single', tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting for Approval'),('approved','Approved'),('reject','Rejected'),('cancel','Cancel')], string='State',default="draft",copy=False,tracking=True)

    # Employment details
    designation = fields.Char(string="Designation on Offer Letter",tracking=True)
    doj = fields.Date(string="Projected Date of Joining",tracking=True)
    employment_duration = fields.Many2one('employment.duration',string="Duration of Employment *",tracking=True)
    probation_term = fields.Char(string="Probation Term",tracking=True)
    notice_period = fields.Char(string="Notice Period",tracking=True)
    working_days = fields.Char(string="Working Days *")
    working_hours = fields.Char(string="Working Hours *")
    annual_vacation = fields.Char(string="Annual Vacation *")
    weekly_off_days = fields.Char(string="Weekly Off (No. Of Days)",tracking=True)

    client_id = fields.Many2one('res.partner',string="Client",default=lambda self: self.env.user.partner_id)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.user.company_id)
    currency_id = fields.Many2one(related='company_id.currency_id', store=True, readonly=True)

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
    

    service_request_type_id = fields.Many2one('ev.service.request.type',string="Service Request Type")
    salary_line_ids = fields.One2many('salary.line', 'emp_visa_id', string="Salary Structure")
    @api.model
    def default_get(self,fields):
        res = super(EmploymentVisa,self).default_get(fields)
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
    approver_id = fields.Many2one('hr.employee',string="Approver")

    # Profession Details
    visa_profession = fields.Char(string="Visa Profession *")
    visa_religion = fields.Selection([('muslim','Muslim'),('non_muslim','Non-Muslim'),('others','Others')],string="Visa Religion *")
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
    insurance_class = fields.Selection([('class_vip+','VIP+'),('class_vip','VIP'),('class_a','A'),('class_b','B'),('class_c','C'),('class_e','E')],string="Class *")
    dependent_document_ids = fields.One2many('dependent.documents','ev_dependent_document_id',string="Dependent Documents")

    @api.onchange('candidate_id')
    def onchange_candidate_update_data(self):
        for line in self:
            if line.candidate_id:
                line.nationality_id = line.candidate_id.nationality_id
                line.email = line.candidate_id.email
                line.marital = line.candidate_id.marital
                line.employment_duration = line.candidate_id.employment_duration
                line.probation_term = line.candidate_id.probation_term
                line.notice_period = line.candidate_id.notice_period
                line.weekly_off_days = line.candidate_id.weekly_off_days
                line.doj = line.candidate_id.doj
                line.work_location_id = line.candidate_id.work_location_id
                line.dob = line.candidate_id.dob
                line.contact_no = line.candidate_id.contact_no
                line.current_contact = line.candidate_id.current_contact


    def unlink(self):
        """
            Delete/ remove selected record
            :return: Deleted record ID
        """
        for objects in self:
            if objects.state in ['waiting', 'approved', 'rejected']:
                raise UserError(_('You cannot remove the record which is in %s state!') % objects.state)
        return super(LocalTransfer, self).unlink()

    

    @api.model_create_multi
    def create(self,vals_list):
        for vals in vals_list:
            vals['name'] = self.env['ir.sequence'].next_by_code('employment.visa')
        res = super(EmploymentVisa,self).create(vals_list)
        return res

    def _add_followers(self):
        """
            Add Approver as followers
        """
        partner_ids = []
        if self.approver_id:
            partner_ids.append(self.approver_id.user_id.partner_id.id)
        self.message_subscribe(partner_ids=partner_ids)

    def action_submit(self):
        # categ_ids = [x.id for x in list(self.category_id)]
        # preffered_location_ids = [x.id for x in list(self.preffered_location_id)]
        
        date = fields.Date.today()
        
        # vals = {
        #     'client_id': self.client_id.id,
        #     'emp_visa_id': self.id,
        #     'candidate_id':self.candidate_id.id,
        #     # 'category_id':[(6, 0, categ_ids)],
        #     # 'preffered_location_id':[(6, 0, preffered_location_ids)],
        #     'designation':self.designation,
        #     'salary_line_ids':[(6, 0, [salary.id for salary in self.salary_line_ids])],
        #     'document_line_ids':[(6, 0, [doc.id for doc in self.document_line_ids])],
        #     'doj':self.doj,
        #     'employment_duration':self.employment_duration.id,
        #     'probation_term':self.probation_term,
        #     'notice_period':self.notice_period,
        #     'weekly_off_days':self.weekly_off_days,
        #     'service_request_type_id':self.service_request_type_id.id,
        #     'document_creation_date':date,
        #     'approver_id':self.client_id.company_spoc_id.id,
        # }
        # service_request_approval_id = self.env['employment.visa.approval'].sudo().create(vals)
        if not self.employment_duration:
            raise UserError(_('Please add Duration of Employment!'))
        if not self.visa_profession:
            raise UserError(_('Please add Visa Profession!'))
        if not self.visa_religion:
            raise UserError(_('Please add Visa Religion!'))
        if not self.visa_nationality_id:
            raise UserError(_('Please add Visa Nationality!'))
        if not self.visa_stamping_city_id:
            raise UserError(_('Please add Visa Stamping City!'))
        if not self.visa_enjaz:
            raise UserError(_('Please add Visa Enjaz Details!'))
        if not self.no_of_visa:
            raise UserError(_('Please add No of Visa!'))
        if not self.visa_gender:
            raise UserError(_('Please add Visa Gender!'))
        if not self.qualification:
            raise UserError(_('Please add Education Qualification!'))
        if not self.email:
            raise UserError(_("Please add Email Id"))
        if not self.current_contact:
            raise UserError(_("Please add Current Contact # (if Outside the country)"))
        if not self.working_days:
            raise UserError(_("Please add Working Days"))
        if not self.working_hours:
            raise UserError(_("Please add Working Hours"))
        if not self.annual_vacation:
            raise UserError(_("Please add Annual Vacation"))
        if not self.insurance_class:
            raise UserError(_("Please select medical Insurance class"))
        if not self.signed_offer_letter:
            raise UserError(_("Please attach Signed Offer letter"))
        if not self.passport_copy:
            raise UserError(_("Please attach Passport Copy"))
        if not self.border_copy:
            raise UserError(_("Please attach Border Id"))
        if not self.attested_degree:
            raise UserError(_("Please attach Attested Degree Copy"))
        if not self.attested_visa_page:
            raise UserError(_("Please attach Attested Visa page"))
        if not self.bank_iban_letter:
            raise UserError(_("Please attach Bank Iban Letter"))
        if not self.certificate_1:
            raise UserError(_("Please attach Certificate"))







        self._add_followers()
        self.approver_id = self.client_id.company_spoc_id.id 
        self.state = 'waiting'

    def action_approve(self):
        for line in self:
            line.state = 'approved'

    def action_reject(self):
        for line in self:
            line.state = 'reject'


    def action_cancel(self):
        for line in self:
            line.state = 'cancel'

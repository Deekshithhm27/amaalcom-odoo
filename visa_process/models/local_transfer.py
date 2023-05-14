# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError,UserError
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class LocalTransfer(models.Model):
    _name = 'local.transfer'
    _order = 'id desc'
    _inherit = ['mail.thread']
    _rec_name = 'name'
    _description = "Local Transfer"

    
    name = fields.Char(string="Sequence",help="The Unique Sequence no", readonly=True, default='/')


    candidate_id = fields.Many2one('visa.candidate',string="Candidate",tracking=True,required=True)
    dob = fields.Date(string="DOB",related="candidate_id.dob")
    contact_no = fields.Char(string="Cell No. (Absher)")
    email = fields.Char(string="Email Id",tracking=True,related="candidate_id.email")
    nationality_id = fields.Many2one('res.country',string="Nationality",tracking=True,related="candidate_id.nationality_id")
    marital = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('cohabitant', 'Legal Cohabitant'),
        ('widower', 'Widower'),
        ('divorced', 'Divorced')
    ], string='Marital Status', groups="hr.group_hr_user", default='single', tracking=True,related="candidate_id.marital")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting for Approval'),('approved','Approved'),('reject','Rejected'),('cancel','Cancel')], string='State',default="draft",copy=False,tracking=True)

    # Employment details
    doj = fields.Date(string="Projected Date of Joining",tracking=True,related="candidate_id.doj")
    employment_duration = fields.Many2one('employment.duration',string="Duration of Employment",tracking=True,related="candidate_id.employment_duration")
    working_days = fields.Char(string="Working Days")
    working_hours = fields.Char(string="Working Hours")
    annual_vacation = fields.Char(string="Annual Vacation")

    client_id = fields.Many2one('res.partner',string="Client",default=lambda self: self.env.user.partner_id)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.user.company_id)
    currency_id = fields.Many2one(related='company_id.currency_id', store=True, readonly=True)

    # # Documents
    # document_line_ids = fields.One2many('candidate.documents.line','service_request_id',string="Documents")
    passport_size_photo = fields.Binary(string="Passport Size Photo")
    dependents_if_any = fields.Binary(string="Dependents if any")
    signed_offer_letter = fields.Binary(string="Signed Offer Letter")
    
    service_request_type_id = fields.Many2one('lt.service.request.type',string="Service Request Type",required=True,tracking=True)
    salary_line_ids = fields.One2many('salary.line', 'local_transfer_id', string="Salary Structure")
    approver_id = fields.Many2one('hr.employee',string="Approver")

    # Profession Details
    profession_en = fields.Char(string="Profession En.")
    profession_arabic = fields.Char(string="Profession Ar.")
    qualification = fields.Char(string="Education Qualification")

    iqama = fields.Char(string="Iqama")
    expiry_date = fields.Date(string="Expiry Date")
    
    work_location_id = fields.Many2one('hr.work.location',string="Work Location",related="candidate_id.work_location_id")

    # Air Fare
    air_fare_for = fields.Selection([('self','Self'),('family','Family')],string="Air Fare for?")
    air_fare_cost = fields.Monetary(string="Air Fare Cost",default=0.0, currency_field='currency_id')
    air_fare_frequency = fields.Char(string="Air Fare Frequency")

    # Medical Insurance
    medical_insurance_for = fields.Selection([('self','Self'),('family','Family')],string="Medical Insurance For?")
    visa_cost = fields.Monetary(string="Visa cost for family members(Self or company - Specify)",default=0.0, currency_field='currency_id')

    # Bank details
    bank_id = fields.Many2one('res.bank')
    bic = fields.Char(string="IBAN")

    notes = fields.Text(string="Notes")


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
            vals['name'] = self.env['ir.sequence'].next_by_code('local.transfer')
        res = super(LocalTransfer,self).create(vals_list)
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
        #     'service_req_id': self.id,
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
        # service_request_approval_id = self.env['local.transfer.approval'].sudo().create(vals)
        if not self.employment_duration:
            raise UserError(_('Please add Duration of Employment!'))
        if not self.qualification:
            raise UserError(_('Please add Education Qualification!'))
        if not self.email:
            raise UserError(_("Please add Email Id"))
        if not self.signed_offer_letter:
            raise UserError(_("Please attach signed offer letter"))
        if not self.dob:
            raise UserError(_("Please add Birth date"))
        if not self.working_days:
            raise UserError(_("Please add Working Days"))
        if not self.working_hours:
            raise UserError(_("Please add Working Hours"))
        if not self.annual_vacation:
            raise UserError(_("Please add Annual Vacation"))
        if not self.bank_id:
            raise UserError(_("Please add Bank"))
        if not self.bic:
            raise UserError(_("Please add IBAN"))








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

# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class ServiceRequest(models.Model):
    _name = 'service.request'
    _order = 'id desc'
    _inherit = ['mail.thread']
    _rec_name = 'name'
    _description = "Visa Service Request"

    name = fields.Char(string="Sequence",help="The Unique Sequence no", readonly=True, default='/')
    candidate_id = fields.Many2one('visa.candidate',string="Candidate",tracking=True,required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting for Approval'),('approved','Approved'),('reject','Rejected'),('cancel','Cancel')], string='State',default="draft",copy=False,tracking=True)

    # Employment details
    designation = fields.Char(string="Designation on Offer Letter",tracking=True)
    doj = fields.Date(string="Projected Date of Joining",tracking=True)
    employment_duration = fields.Many2one('employment.duration',string="Duration of Employment")
    probation_term = fields.Char(string="Probation Term")
    notice_period = fields.Char(string="Notice Period")
    weekly_off_days = fields.Char(string="Weekly Off (No. Of Days)")

    client_id = fields.Many2one('res.partner',string="Client",default=lambda self: self.env.user.partner_id)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.user.company_id)

    # Documents
    document_line_ids = fields.One2many('candidate.documents.line','service_request_id',string="Documents")
    service_request_type_id = fields.Many2one('service.request.type',string="Service Request Type",required=True,tracking=True)
    salary_line_ids = fields.One2many('salary.line', 'service_req_id', string="Salary Structure")
    approver_id = fields.Many2one('hr.employee',string="Approver")

    

    @api.model_create_multi
    def create(self,vals_list):
        for vals in vals_list:
            candidate_code = self.env['ir.sequence'].next_by_code('service.request')
            client_id = self.env['res.partner'].search([('id','=',self.env.user.partner_id.id)])
            candidate_code = candidate_code.replace("SERVICE_REQUEST_SEQUENCE", 'SR-'+ client_id.client_code + '-')
            vals["name"] = candidate_code
        res = super().create(vals_list)
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
        # service_request_approval_id = self.env['service.request.approval'].sudo().create(vals)
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

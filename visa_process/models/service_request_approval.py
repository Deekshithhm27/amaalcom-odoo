# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class ServiceRequestApproval(models.Model):
    _name = 'service.request.approval'
    _order = 'id desc'
    _inherit = ['mail.thread']
    _rec_name = 'name'
    _description = "Visa Service Request Approval"

    name = fields.Char(string="Sequence",help="The Unique Sequence no", readonly=True, default='/')
    candidate_id = fields.Many2one('visa.candidate',string="Candidate",tracking=True,required=True)

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
    document_line_ids = fields.One2many('candidate.documents.line','service_request_approval_id',string="Documents")
    service_request_type_id = fields.Many2one('service.request.type',string="Service Request Type",required=True,tracking=True)
    salary_line_ids = fields.One2many('salary.line', 'service_req_approval_id', string="Salary Structure")

    service_req_id = fields.Many2one('service.request',string="Service Request")
    document_creation_date = fields.Date(string="Creation Date")
    approver_id = fields.Many2one('hr.employee',string="Approver")

    @api.model_create_multi
    def create(self,vals_list):
        for vals in vals_list:
            candidate_code = self.env['ir.sequence'].next_by_code('service.request.approval')
            vals["name"] = candidate_code
        res = super().create(vals_list)
        return res

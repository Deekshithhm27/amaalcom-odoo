# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class VisaCandidate(models.Model):
    _name = 'visa.candidate'
    _order = 'id desc'
    _inherit = ['mail.thread']
    _rec_name = 'name'
    _description = "Visa Candidate data"

    name = fields.Char(string="Name",tracking=True,copy=False)
    sequence = fields.Char(string="Sequence",help="The Unique Sequence no", readonly=True, default='/')
    surname = fields.Char(string="Surname",tracking=True)
    given_name = fields.Char(string="Given Name",tracking=True)
    email = fields.Char(string="Email Id",tracking=True,required=True)
    dob = fields.Date(string="DOB",tracking=True,required=True)
    nationality_id = fields.Many2one('res.country',string="Nationality",tracking=True)
    
    
    contact_no = fields.Char(string="Contact # in the country")
    current_contact = fields.Char(string="Current Contact # (if Outside the country)")
    marital = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('cohabitant', 'Legal Cohabitant'),
        ('widower', 'Widower'),
        ('divorced', 'Divorced')
    ], string='Marital Status', groups="hr.group_hr_user", default='single', tracking=True)
    work_location_id = fields.Many2one('hr.work.location',string="Work Location")
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.user.company_id)
    client_id = fields.Many2one('res.partner',string="Client",default=lambda self: self.env.user.partner_id)

    resume_line_ids = fields.One2many('hr.resume.line', 'candidate_id', string="Resumé lines")
    employee_skill_ids = fields.One2many('hr.employee.skill', 'candidate_id', string="Skills")

    
    doj = fields.Date(string="Projected Date of Joining",tracking=True)
    employment_duration = fields.Many2one('employment.duration',string="Duration of Employment",tracking=True)
    probation_term = fields.Char(string="Probation Term")
    notice_period = fields.Char(string="Notice Period")
    working_days = fields.Char(string="Working Days")
    weekly_off_days = fields.Char(string="Weekly Off (No. Of Days)")

    @api.model_create_multi
    def create(self, vals_list):
        resume_lines_values = []
        for employee in res:
            line_type = self.env.ref('hr_skills.resume_type_experience', raise_if_not_found=False)
            resume_lines_values.append({
                'candidate_id': employee.id,
                'name': employee.company_id.name or '',
                'date_start': employee.create_date.date(),
                'line_type_id': line_type and line_type.id,
            })
        self.env['hr.resume.line'].create(resume_lines_values)
        return res


    # @api.model
    # def create(self, values):
    #     res = super(VisaCandidate, self).create(values)
    #     client_seq = self.env.user.partner_id
    #     res.sequence = client_seq.next_code
    #     res.sequence = str(client_seq.client_code) + '/' + str(client_seq.next_code)
    #     # res.name = '[' + str(client_seq.next_code) + ']' + str(res.name)
    #     client_seq.write({'next_code': int(client_seq.next_code) + 1})
    #         # else:
    #         #     res.sequence = client_seq.client_code
    #         #     res.name = '[' + str(client_seq.client_code) + ']' + str(res.name)
    #         #     client_seq.write({'next_code': client_seq.client_code + 1})
    #     return res

    @api.model_create_multi
    def create(self,vals_list):
        for vals in vals_list:
            candidate_code = self.env['ir.sequence'].next_by_code('visa.candidate')
            client_id = self.env['res.partner'].search([('id','=',self.env.user.partner_id.id)])
            candidate_code = candidate_code.replace("CLIENT_SEQUENCE", client_id.client_code + '-')
            vals["sequence"] = candidate_code
        res = super().create(vals_list)
        return res



# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    sequence = fields.Char(string="Sequence",help="The Unique Sequence no", readonly=True, default='/')
    
    surname = fields.Char(string="Surname",tracking=True)
    given_name = fields.Char(string="Given Name",tracking=True)
    # replaced to birthday
    # nationality_id = fields.Many2one('res.country',string="Nationality",tracking=True)
    # replaces to country id
    
    
    contact_no = fields.Char(string="Contact # in the country")
    phone_code_id = fields.Many2one('res.partner.phonecode',string="Phone code")

    current_contact = fields.Char(string="Current Contact # (if Outside the country)")
    current_phone_code_id = fields.Many2one('res.partner.phonecode',string="Phone code")

    religion = fields.Selection([('muslim','Muslim'),('non_muslim','Non-Muslim'),('others','Others')],string="Religion")

    client_id = fields.Many2one('res.partner',string="Client")

    iqama_certificate = fields.Binary(string="Iqama")
    degree_certificate = fields.Binary(string="Degree")


    
    doj = fields.Date(string="Projected Date of Joining",tracking=True)

    employment_duration = fields.Many2one('employment.duration',string="Duration of Employment",tracking=True)
    probation_term = fields.Char(string="Probation Term")
    notice_period = fields.Char(string="Notice Period")
    working_days = fields.Char(string="Working Days")
    weekly_off_days = fields.Char(string="Weekly Off (No. Of Days)")

    
    

    iqama = fields.Char(string="Designation on Iqama")

    # This field is to differentiate between internal and external (client) employees
    employee_type = fields.Selection([('external','External'),('internal','Internal')],string="Type of user to set System Access",default=lambda self: self.env.user.user_type)


    @api.model
    def create(self, vals):
        vals['sequence'] = self.env['ir.sequence'].next_by_code('hr.employee')
        if vals.get('user_id'):
            user = self.env['res.users'].browse(vals['user_id'])
            vals['employee_type'] = user.user_type


        employee = super(HrEmployee, self).create(vals)
        return employee




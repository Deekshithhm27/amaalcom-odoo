# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class SalaryLines(models.Model):
    _name = "salary.line"
    _order = 'id desc'
    _inherit = ['mail.thread']
    _rec_name = 'name'

    name = fields.Many2one('salary.structure',string="Structure Type")

    emp_visa_id = fields.Many2one('employment.visa',string="Employment Visa Id")
    ev_enq_visa_id = fields.Many2one('service.enquiry',string="EV Service Enquiry")
    local_transfer_id = fields.Many2one('local.transfer',string="Local Transfer Id")
    
    amount = fields.Float(string="Amount")

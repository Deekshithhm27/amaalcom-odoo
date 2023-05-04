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

    service_req_id = fields.Many2one('service.request',string="Service request Id")
    service_req_approval_id = fields.Many2one('service.request.approval',string="Service request Approval Id")
    name = fields.Many2one('salary.structure',string="Structure Type")
    amount = fields.Float(string="Amount")

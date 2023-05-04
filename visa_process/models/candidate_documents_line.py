# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class CandidateDocumentsLine(models.Model):
    _name = "candidate.documents.line"
    _description = "Candidate Documents Line"

    service_request_id = fields.Many2one('service.request',string="Service Request id")
    service_request_approval_id = fields.Many2one('service.request.approval',string="Service Request Approval id")
    
    name = fields.Many2one('visa.candidate.documents',string="Document Type")
    document_availability = fields.Boolean(string="Availability")
    document_file = fields.Binary(string="Document")

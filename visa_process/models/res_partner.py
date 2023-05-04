# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime
from dateutil import relativedelta as rdelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class ResPartner(models.Model):
    _inherit = 'res.partner'

    client_code = fields.Char(string="Client Code")
    next_code = fields.Char(string='Next code',copy=False,default="00001")

    candidates_count = fields.Integer(compute='_compute_candidates_count')
    service_req_count = fields.Integer(compute='_compute_service_req_count')

    company_spoc_id = fields.Many2one('hr.employee',string="Accounts Manager",required=True,tracking=True)


    # def _fetch_candidates(self):
    #   candidate_id = self.env['visa.candidate'].search([('client_id','=',self.id)])
    #   if candidate_id:
    #       for line in self:
    #           candidate_ids.

 

    def _compute_candidates_count(self):
        for line in self:
            candidate_id = self.env['visa.candidate'].search([('client_id', '=', line.id)])
            line.candidates_count = len(candidate_id)

    def _compute_service_req_count(self):
        for line in self:
            service_rq_id = self.env['service.request'].search([('client_id', '=', line.id)])
            line.service_req_count = len(service_rq_id)

    
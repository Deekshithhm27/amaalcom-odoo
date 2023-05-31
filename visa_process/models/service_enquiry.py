# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError,UserError
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class ServiceEnquiry(models.Model):
    _name = 'service.enquiry'
    _order = 'id desc'
    _inherit = ['mail.thread']
    _rec_name = 'name'
    _description = "Service Enquiry"

    name = fields.Char(string="Enquiry No")
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.user.company_id)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting','Waiting for Response'),
        ('done', 'Done'),('refuse','Refuse'),('cancel','Cancel')], string='State',default="draft",copy=False,tracking=True)
    service_request = fields.Selection([('lt_request','Local Transfer'),('ev_request','Employment Visa')],string="Service Request",default='lt_request')
    ev_service_request_type_id = fields.Many2one('ev.service.request.type',string="Service Request Type")
    lt_service_request_type_id = fields.Many2one('lt.service.request.type',string="Service Request Type")
    candidate_id = fields.Many2one('visa.candidate',string="Candidate")

    client_id = fields.Many2one('res.partner',string="Client",default=lambda self: self.env.user.partner_id)
    approver_id = fields.Many2one('hr.employee',string="Approver")

    request_note = fields.Text(string="Request Query")    

    @api.onchange('service_request')
    def update_service_request(self):
        for line in self:
            if line.service_request == 'en_request':
                print("---en")
                line.lt_service_request_type_id = False
            if line.service_request == 'lt_request':
                print("--lt")
                line.ev_service_request_type_id = False

    def action_submit(self):
        for line in self:
            line.state = 'waiting'
            self.approver_id = self.client_id.company_spoc_id.id 
            self._add_followers()

    def action_confirm(self):
        for line in self:
            line.state = 'done'

    def action_refuse(self):
        for line in self:
            line.state = 'refuse'

    def action_cancel(self):
        for line in self:
            line.state = 'cancel'

    @api.model_create_multi
    def create(self,vals_list):
        for vals in vals_list:
            vals['name'] = self.env['ir.sequence'].next_by_code('service.enquiry')
        res = super(ServiceEnquiry,self).create(vals_list)
        return res

    def _add_followers(self):
        """
            Add Approver as followers
        """
        partner_ids = []
        if self.approver_id:
            partner_ids.append(self.approver_id.user_id.partner_id.id)
        self.message_subscribe(partner_ids=partner_ids)

    def action_create_service_request(self):
        print("------------")
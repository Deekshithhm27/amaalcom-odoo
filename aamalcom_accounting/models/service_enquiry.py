# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError,UserError
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class ServiceEnquiry(models.Model):
    _inherit = 'service.enquiry'
    
    create_payment_request = fields.Boolean(string="Create Payment Request",store=True,compute="update_create_payment_request")

    @api.depends('self_bill')
    def update_create_payment_request(self):
        for line in self:
            if line.self_bill:
                line.create_payment_request = True
            else:
                line.create_payment_request = False

    def action_create_payment_req(self):
        vals = {
            'client_id': self.client_id.id,
            'employee_id':self.employee_id.id,
            'amount':self.total_amount,
            'service_enquiry_id':self.id
        }
        payment_approval_id = self.env['account.payment.approval'].sudo().create(vals)

    payments_count = fields.Integer(compute='_compute_payments_count')

    def _compute_payments_count(self):
        for line in self:
            payment_id = self.env['account.payment.approval'].search([('service_enquiry_id', '=', line.id)])
            line.payments_count = len(payment_id)

        
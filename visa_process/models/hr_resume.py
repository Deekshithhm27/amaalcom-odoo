# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class Employee(models.Model):
    _inherit = 'hr.resume.line'
    
    candidate_id = fields.Many2one('visa.candidate', required=False, ondelete='cascade')
    employee_id = fields.Many2one('hr.employee', required=False, ondelete='cascade')

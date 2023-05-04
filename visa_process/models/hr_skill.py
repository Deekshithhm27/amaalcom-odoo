# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class EmployeeSkill(models.Model):
    _inherit = 'hr.employee.skill'
    
    candidate_id = fields.Many2one('visa.candidate', required=False, ondelete='cascade')
    employee_id = fields.Many2one('hr.employee', required=False, ondelete='cascade')

    # _sql_constraints = [
    #     ('_unique_skill', 'unique (candidate_id, skill_id)', "Two levels for the same skill is not allowed"),
    # ]
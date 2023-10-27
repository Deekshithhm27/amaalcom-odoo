# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError,UserError
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class LocalTransfer(models.Model):
    _inherit = 'local.transfer'
    

    @api.model
    def default_get(self,fields):
        res = super(LocalTransfer,self).default_get(fields)
        salary_lines = [(5,0,0)]
        salary_ids = self.env['hr.client.salary.rule'].search([])
        for sal in salary_ids:
            line = (0,0,{
                'name':sal.id
                })
            salary_lines.append(line)
        res.update({
            'client_salary_rule_ids':salary_lines
            })
        return res

    client_salary_rule_ids = fields.One2many('salary.line', 'local_transfer_id', string="Salary Structure")
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class ResUsers(models.Model):
    _inherit = "res.users"

    user_type = fields.Selection([('external','External'),('internal','Internal')],string="Type of user to set System Access",required=True)
    partner_company_id = fields.Many2one('res.partner',string="Company",domain="[('is_company','=',True)]")

    company_spoc_id = fields.Many2one('hr.employee',string="Accounts Manager",domain="[('custom_employee_type','=','internal')]")


    def action_create_employee(self):
        self.ensure_one()
        self.env['hr.employee'].create(dict(
            name=self.name,
            company_id=self.env.company.id,
            **self.env['hr.employee']._sync_user(self)
        ))
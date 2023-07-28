# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class LetterPrintType(models.Model):
    _name = "letter.print.type"
    _description = "Letter Print Type"
    _inherit = ['mail.thread']

    name = fields.Char(string="Type")
    # print_type = fields.Selection([('coc','COC'),('letterhead','Letter head'),('mofa','MOFA')],string="Type")
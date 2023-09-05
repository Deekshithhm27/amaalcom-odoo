# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError,UserError
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class DraftInvoiceSequence(models.Model):
    _name = 'draft.invoice.sequence'
    _description = 'Draft Invoice Sequence'

    sequence = fields.Integer(string='Next Sequence', default='00001')



class AccountMove(models.Model):
    _inherit = 'account.move'
 
    draft_invoice_sequence_id = fields.Many2one('draft.invoice.sequence', string='Draft Invoice Sequence', readonly=True, copy=False)
    draft_invoice_sequence = fields.Integer(related='draft_invoice_sequence_id.sequence', string='Draft Invoice Sequence Number', readonly=True, store=True)
    state = fields.Selection(selection=[('draft', 'Draft'),
            ('approval_needed', 'Waiting for Approval'),
            ('manager_approval', 'Waiting for Manager Approval'),
            ('approved', 'Approved'),
            ('posted', 'Posted'),
            ('cancel', 'Cancelled')], string='Status', required=True, readonly=True, copy=False, tracking=True,
        default='draft')

    @api.model
    def create(self, vals):
        if vals.get('state') == 'draft':
            sequence_id = self.env['draft.invoice.sequence'].search([], limit=1)
            if sequence_id:
                vals['draft_invoice_sequence_id'] = sequence_id.id
                vals['name'] = 'DI/' + sequence_id.sequence.zfill(5)
                sequence_id.sequence = str(int(sequence_id.sequence) + 1).zfill(5)
        return super(AccountMove, self).create(vals)


    def unlink(self):
        for invoice in self:
            if invoice.state == 'draft' and invoice.draft_invoice_sequence_id:
                invoice.draft_invoice_sequence_id.sequence = str(int(invoice.draft_invoice_sequence_id.sequence) - 1).zfill(5)
        return super(AccountMove, self).unlink()

    def action_submit_for_approval(self):
        for line in self:
            if not line.line_ids.filtered(lambda line: not line.display_type):
                raise UserError(_('You need to add a line before posting.'))
            line.state = 'approval_needed'

    def action_manager_approval(self):
        for line in self:
            line.state = 'approved'

    
    def action_first_approval(self):
        for line in self:
            line.state = 'manager_approval'

    


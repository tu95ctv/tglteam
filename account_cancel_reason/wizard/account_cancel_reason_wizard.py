# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ReasonWizard(models.TransientModel):
    _name = 'account.cancel.reason.wizard'

    reason_id = fields.Many2one('account.cancel.reason', string="Cancel Reason")
    reason_attachment = fields.Binary(string="Cancel Reason Attachment")
    reason_attachment_filename = fields.Char()
    cancel_type = fields.Char()

    @api.multi
    def cancel_invoice(self):
        invoices = self.env['account.invoice'].browse(self._context.get('active_ids', []))
        invoices.write({'reason_id': self.reason_id.id,
            'reason_attachment':self.reason_attachment,
            'reason_attachment_filename': self.reason_attachment_filename
            })
        invoices.with_context(is_in_wizard=True).action_invoice_cancel()


    @api.multi
    def cancel_payment(self):
        payments = self.env['account.payment'].browse(self._context.get('active_ids', []))
        payments.write({'reason_id': self.reason_id.id,
            'reason_attachment':self.reason_attachment,
            'reason_attachment_filename': self.reason_attachment_filename
            })
        payments.with_context(is_in_wizard=True).cancel()


    
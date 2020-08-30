# -*- coding: utf-8 -*-
import base64
from odoo import models, fields, api
from odoo.exceptions import UserError

class AccountCancelReason(models.Model):
    _name = 'account.cancel.reason'

    name = fields.Char()

class account_payment(models.Model):
    _inherit = "account.payment"

    reason_id = fields.Many2one('account.cancel.reason', readonly=1, string="Cancel Reason")
    reason_attachment = fields.Binary(readonly=1, string="Cancel Reason Attachment")
    reason_attachment_filename = fields.Char(readonly=1)

    @api.multi
    def cancel(self):
        if not self._context.get('is_in_wizard'):
            reason_wizard_action = self.env.ref('account_cancel_reason.account_cancel_reason_wizard_action').read()[0]
            reason_wizard_action['context']= {'default_cancel_type':'payment'}
            return reason_wizard_action
        else:
            for payment in self:
                if not payment.reason_id:
                    raise UserError('payment chua co truong reason id')
                else:
                    payment.message_post(body=payment.reason_id.name,
                        subject=payment.reason_id.name,
                        attachments=[(payment.reason_attachment_filename, base64.b64decode(payment.reason_attachment))] if payment.reason_attachment else None
                    )
                    return super(account_payment, self).cancel()

        
class AccountInvoice(models.Model):    
    _inherit = "account.invoice"
    
    reason_id = fields.Many2one('account.cancel.reason', readonly=1, string="Cancel Reason")
    reason_attachment = fields.Binary(readonly=1, string="Cancel Reason Attachment")
    reason_attachment_filename = fields.Char(readonly=1)
    
    def action_invoice_cancel(self):
        if not self._context.get('is_in_wizard'):
            reason_wizard_action = self.env.ref('account_cancel_reason.account_cancel_reason_wizard_action').read()[0]
            reason_wizard_action['context']= {'default_cancel_type':'invoice'}
            return reason_wizard_action
        else:
            return super(AccountInvoice, self).action_invoice_cancel()

    @api.multi
    def action_cancel(self):
        for inv in self:
            if not inv.reason_id:
                raise UserError('chua co truong reason id')
            else:
                inv.message_post(body=inv.reason_id.name,
                    subject=inv.reason_id.name,
                    attachments=[(inv.reason_attachment_filename, base64.b64decode(inv.reason_attachment))] if inv.reason_attachment else None
                )
               
                return super(AccountInvoice, self).action_cancel()

        





    


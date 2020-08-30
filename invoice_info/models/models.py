# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    invoice_total = fields.Float(compute='_compute_invoice_total', store=True)
    invoice_paid = fields.Float(compute='_compute_invoice_paid', store=True)
    invoice_liabilities = fields.Float(compute='_compute_invoice_liabilities', store=True)
    sale_liabilities = fields.Float(compute='_compute_sale_liabilities', store=True)

    @api.depends('invoice_ids.amount_total')
    def _compute_invoice_total(self):
        for r in self:
            # r.invoice_total = sum(r.invoice_ids.filtered(lambda r: r.state != 'cancel').mapped('amount_total'))
            # invoices = r.invoice_ids.filtered(lambda r: r.state != 'cancel')
            invoices = self.env['account.invoice'].search([('id', 'in', r.invoice_ids.ids), ('state','!=', 'cancel')])
            r.invoice_total = sum(invoices.mapped('amount_total'))

    @api.depends('invoice_ids.residual', 'invoice_ids.amount_total')
    def _compute_invoice_liabilities(self):
        for r in self:
            # validate_invoices = r.invoice_ids.filtered(lambda r: r.state != 'cancel' and r.state != 'draft')
            # draft_invoices = r.invoice_ids.filtered(lambda r: r.state != 'cancel' and r.state == 'draft')
            validate_invoices = self.env['account.invoice'].search([('id', 'in', r.invoice_ids.ids), ('state','!=', 'cancel'), ('state','!=', 'draft')])
            draft_invoices = self.env['account.invoice'].search([('id', 'in', r.invoice_ids.ids), ('state','!=', 'cancel'), ('state','=', 'draft')])
            r.invoice_liabilities = sum(validate_invoices.mapped('residual')) +\
                sum(draft_invoices.mapped('amount_total'))
    
    @api.depends('invoice_total', 'invoice_liabilities')
    def _compute_invoice_paid(self):
        for r in self:
            r.invoice_paid = r.invoice_total - r.invoice_liabilities
    
    @api.depends('amount_total', 'invoice_paid')
    def _compute_sale_liabilities(self):
        for r in self:
            r.sale_liabilities = r.amount_total - r.invoice_paid

       



     


# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PaymentTracking(models.Model):
    _inherit = "account.payment"

    amount = fields.Monetary(string='Payment Amount', required=True, track_visibility='onchange')
    partner_id = fields.Many2one(track_visibility='onchange')
    communication = fields.Char(string='Memo', track_visibility='onchange')


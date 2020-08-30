# -*- coding: utf-8 -*-
import base64
from odoo import models, fields, api
from odoo.exceptions import UserError
import urllib.request
import ssl
import xml.etree.ElementTree as ET

class CurrencyRateDayHistory(models.Model):
    _name = 'currency.rate.day.history'
    _order = 'fetch_time desc, id desc'
    # currency_id = fields.Many2one('res.currency')
    rate_id = fields.Many2one('res.currency.rate', string="Currency Rate")
    fetch_time = fields.Datetime(string="Rate")
    
    @api.onchange('reverse_rate')
    def _onchange_reverse_rate(self):
        self.rate = 1.0 / (self.reverse_rate or 1.0)

    rate = fields.Float('Rate', digits=(12, 20), help='The rate of the currency to the currency of rate 1')
    reverse_rate = fields.Integer('Reverse Rate')

class ResCurrencyRate(models.Model):
    _inherit = 'res.currency.rate'

    rate_day_history_ids = fields.One2many('currency.rate.day.history', 'rate_id')
    







   







    


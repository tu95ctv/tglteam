# -*- coding: utf-8 -*-
import base64
from odoo import models, fields, api
from odoo.exceptions import UserError
import urllib.request
import ssl
import xml.etree.ElementTree as ET
import pytz
import datetime
from odoo.tools import float_compare
def convert_vn_native_time_to_utc_tz(datetime_input):
    local = pytz.timezone("Asia/Ho_Chi_Minh")
    local_dt = local.localize(datetime_input, is_dst=None)
    utc_dt = local_dt.astimezone (pytz.utc)
    return utc_dt

class ResCurrency(models.Model):
    _inherit = 'res.currency'

    def update_currency_rate(self, is_single=True):
        root = self.get_vcb_root()
        format = '%m/%d/%Y %H:%M:%S %p'
        rs = root.findall("DateTime")[0]
        st_datetime_vcb = rs.text
        native_datetime_vcb = datetime.datetime.strptime(st_datetime_vcb, format)
        utc_datetime_vcb = native_datetime_vcb
        utc_datetime_vcb = convert_vn_native_time_to_utc_tz(native_datetime_vcb)
        if is_single:
            currency = self
        expr = ".//Exrate[@CurrencyCode='%s']"%self.name if is_single else 'Exrate'
        exrate_nodes = root.findall(expr)
        
        if not exrate_nodes:
            if is_single:
                raise UserError('Không tồn tại tỉ giá %s'%self.name)
        RateObj = self.env['res.currency.rate']
        RateHistoryObj = self.env['currency.rate.day.history']
        for child in exrate_nodes:
            transfer = child.get('Transfer')
            transfer = float(transfer.replace(',', ''))
            if not is_single:
                currencyCode = child.get('CurrencyCode')
                currency = self.search([
                    '|',
                    ('active','=', False), 
                    ('active','=', True),
                    ('name','=', currencyCode),
                ])
                if not currency:
                    continue
            rate = 1.0/transfer
            currency_rate = RateObj.search([
                    ('currency_id','=',currency.id), 
                    ('name','=', native_datetime_vcb.date())
                    ], limit=1)
            if not currency_rate:
                currency_rate = RateObj.create({
                    'currency_id': currency.id, 
                    'name':native_datetime_vcb.date(), 
                    'rate':rate,
                    'reverse_rate': transfer,
                })
            else:
                currency_rate.rate = rate
                currency_rate.reverse_rate = transfer
            history_last = RateHistoryObj.search([
                ('rate_id','=',currency_rate.id)
            ], order='id desc', limit=1)
            if not history_last or float_compare(history_last.rate, rate, precision_rounding=20):
                RateHistoryObj.create({
                        'rate_id': currency_rate.id, 
                        'fetch_time':utc_datetime_vcb, 
                        'rate':rate,
                        'reverse_rate': transfer,
                    })

    def get_vcb_root(self):
        url = 'http://portal.vietcombank.com.vn/Usercontrols/TVPortal.TyGia/pXML.aspx'
        context = ssl._create_unverified_context()
        fp = urllib.request.urlopen(url, context=context)
        mybytes = fp.read()
        fp.close()
        mystr = mybytes.decode("utf8")
        root = ET.fromstring(mystr)
        return root

    def fetch_single_rate(self):
        for r in self:
            r.update_currency_rate()
    
    @api.model
    def fetch_all_rate(self):
        self.update_currency_rate(is_single=False)







    


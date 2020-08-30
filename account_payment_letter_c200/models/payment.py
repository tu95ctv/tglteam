# -*- coding: utf-8 -*-
from odoo import api, fields, models
from num2words import num2words

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    def num2words(self, value, lang='vi_VN'):
        return num2words(value, lang=lang).title() + ' đồng'



  
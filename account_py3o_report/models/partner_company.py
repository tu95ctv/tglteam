# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    def display_address_without_name(self, without_company=True):
        return self._display_address(without_company=without_company).replace('\n','')
    

class Company(models.Model):
    _inherit = 'res.company'

    def display_address_without_name(self):
        return self.partner_id._display_address(without_company=True).replace('\n','')
    


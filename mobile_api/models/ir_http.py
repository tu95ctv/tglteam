# -*- coding: utf-8 -*-

from odoo import http
from odoo import models
from odoo.http import request
import requests
import json

class Http(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        res = super(Http, self).session_info()
        pricelist_id = request.env.user.partner_id.property_product_pricelist
        res['pricelist_id'] = pricelist_id and pricelist_id.id or False
        return res

# -*- coding: utf-8 -*-
import base64
from odoo import models, fields, api
from odoo.exceptions import UserError

class ProductTemplate(models.Model):
    _inherit = 'product.product'
    weight = fields.Float(digits=10)
    weight_gam = fields.Float(string="Weight Gam", compute = '_compute_weight_gam', store=True)
    volume_ml = fields.Float(string="Volume ml", compute = '_compute_volume_ml', store=True)
    
    volume = fields.Float(
        'Volume', compute='_compute_volume', inverse='_set_volume',
        help="The volume in m3.", store=True, digits=10)
    weight = fields.Float(
        'Weight', compute='_compute_weight', digits=10,
        inverse='_set_weight', store=True,
        help="The weight of the contents in Kg, not including any packaging, etc.")

    @api.depends('weight')
    def _compute_weight_gam(self):
        for r in self:
            r.weight_gam = 1000*r.weight

    @api.onchange('weight_gam')
    def _ochange_weight_gam(self):
        for r in self:
            r.weight = r.weight_gam / 1000

    @api.depends('volume')
    def _compute_volume_ml(self):
        for r in self:
            if r.volume:
                r.volume_ml = 1000*r.volume

    @api.onchange('volume_ml')
    def _ochange_volume_ml(self):
        for r in self:
            r.volume = r.volume_ml / 1000





        

        





    


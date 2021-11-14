# -*- coding: utf-8 -*-

from odoo import api, fields, models

class IrFilters(models.Model):
    _inherit = 'ir.filters'
    _order = 'sequence, name'

    sequence = fields.Integer(required=True, default=0)
    show_in_tab = fields.Boolean(string='Show in TabView', default=False)

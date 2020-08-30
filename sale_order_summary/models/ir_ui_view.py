# -*- coding: utf-8 -*-

from odoo import models, fields, api

class View(models.Model):

    _inherit = "ir.ui.view"

    is_banner_template = fields.Boolean()
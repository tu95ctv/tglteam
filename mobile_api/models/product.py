# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.tools.safe_eval import safe_eval
from odoo.tools.image import image_data_uri


class ProductTemplateImage(models.Model):
    _name = 'product.template.image'
    _order = 'product_id, sequence'

    sequence = fields.Integer('Sequence')
    product_id = fields.Many2one('product.template', 'Product')
    image = fields.Binary('Image', attachment=True)
    image_url = fields.Char('URL Image')
    note = fields.Text('Note')

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    published_on_app = fields.Boolean('Published on app')
    ecommerce_mobile_app_categ_ids = fields.Many2many('ecommerce.mobile.app.category', 'product_template_id', 'category_id', 'product_id', string='Mobile Category')
    image_url = fields.Char('URL Image')
    image_ids = fields.One2many('product.template.image', 'product_id', 'Mobile images')
    mobile_summury_description = fields.Html('Summury description')
    mobile_detail_description = fields.Html('Detail description')
    mobile_technical_description = fields.Html('Technical description')

class ProductBrand(models.Model):
    _inherit = 'product.brand'

    logo = fields.Binary('Logo File', attachment=True)
    image_url = fields.Char('URL Image')

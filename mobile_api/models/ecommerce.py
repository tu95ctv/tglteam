# -*- coding: utf-8 -*-

from odoo import fields, models, api

class AppCategory(models.Model):
    _name = 'ecommerce.mobile.app.category'
    _description = 'category for mobile apps'
    _order = 'sequence asc'

    name = fields.Char('Name', required=True)
    active = fields.Boolean('Active', default=True)
    sequence = fields.Integer('Sequence')
    parent_id = fields.Many2one('ecommerce.mobile.app.category', string='Parent category')
    type = fields.Selection([('normal', 'Normal'), ('featured', 'Featured category')], 'Type', default='normal', required=True)
    image = fields.Binary('Image', attachment=True)
    image_url = fields.Char('URL Image')


class AppBanner(models.Model):
    _name = 'ecommerce.mobile.app.banner'
    _description = 'banner for mobile apps'
    _order = 'sequence'

    name = fields.Char('Name', required=True)
    active = fields.Boolean('Active', default=True)
    sequence = fields.Integer('Sequence')
    image = fields.Binary('Image')
    image_url = fields.Char('URL Image')
    url = fields.Char('Banner Image Url(Optional)')
    action = fields.Selection([('product', 'Open product page'),
                             ('category', 'Open category page'),
                             ('custom', 'Open custom collection page'),
                             ('none', 'Do nothing')], 'Action to be triggered', default='product', required=True)

    category_id = fields.Many2one('ecommerce.mobile.app.category', 'Choose category')
    publish_date = fields.Date('Publish date')
    description = fields.Text('Description')
    product_ids = fields.Many2many('product.template', 'app_banner_product_template_rel', 'app_banner_id', 'product_id', string='Products')


class AppSlider(models.Model):
    _name = 'ecommerce.mobile.app.slider'
    _description = 'slider for mobile apps'
    _order = 'sequence'

    name = fields.Char('Name', required=True)
    active = fields.Boolean('Active', default=True)
    sequence = fields.Integer('Sequence')
    description = fields.Text('Description')
    product_selection = fields.Selection([('manual', 'Manual'), ('automatic', 'Automatic')], 'Selection Criterial', default='manual', required=True)
    based_on = fields.Selection([('new', 'Newly created'),
                               ('internal_category', 'Internal Category'),
                               ('mobile_category', 'Mobile App Category')], string='Based on')
    product_ids = fields.Many2many('product.template', 'app_slider_product_template_rel', 'app_slider_id', 'product_id', string='Products', domain=[('published_on_app', '=', True)])
    categ_id = fields.Many2one('product.category', string='Internal Category')
    mobile_app_categ_id = fields.Many2one('ecommerce.mobile.app.category', string='Mobile App Category')
    mode = fields.Selection([('default', 'Default (Slide)'), ('fixed', 'fixed')], string='Slider Mode', default='default', required=True)
    product_image_position = fields.Selection([('center', 'Center'), ('right', 'Right'), ('left', 'Left')], default='center', required=True)
    max_product_in_slider = fields.Integer('Max. product in slider')
    product_per_row = fields.Integer('Product per row')

    # pricelist_id = fields.Many2one('product.pricelist', 'Pricelist')
    # item_ids = fields.One2many('product.pricelist.item', 'Pricelist detail', related='pricelist_id.item_ids', readonly=False)


class AppSlider(models.Model):
    _name = 'ecommerce.mobile.more.app'
    _description = 'More application for mobile apps'
    _order = 'sequence'

    sequence = fields.Integer('Sequence')
    title = fields.Char('Title')
    image_url = fields.Char('Image URL')
    open_url = fields.Char('Open URL')

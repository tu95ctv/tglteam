# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools
from odoo.modules import get_module_resource
import base64
from odoo.exceptions import UserError

class ResPartner(models.Model):
    
    _inherit = 'res.partner'

    @api.onchange('product_id')
    def _product_id_onchage(self):
        if self.is_unit:
            self.image = self.product_id.image

    # @api.onchange('relationship_owner_id')
    # def _product_id_onchage(self):
    #     if self.is_unit:
    #         self.image = self.product_id.image

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('is_unit') and vals.get('product_id'):
                image_data =  self.env['product.product'].browse(vals.get('product_id')).image
                vals['image'] = image_data
        return super(ResPartner,self).create(vals_list)
    # @api.model_create_multi
    # def create(self, vals_list):
    #     for vals in vals_list:
    #         if vals.get('is_unit') and 'image' not in vals:
    #             img_path = get_module_resource('buiding_unit_inherit', 'static/img', 'toanha.jpg')
    #             if img_path:
    #                 with open(img_path, 'rb') as f:
    #                     image = f.read()
    #             else:
    #                 raise UserError('Thiếu hình ở buiding_unit_inherit/static/img/toanha.jpg')
    #             image_data =  tools.image_resize_image_big(base64.b64encode(image))
    #             vals['image'] = image_data
    #     return super(ResPartner,self).create(vals_list)



    @api.multi 
    def update_avatar_image(self):
        for r in self:
            img_path = get_module_resource('buiding_unit_inherit', 'static/img', 'toanha.jpg')
            if img_path:
                with open(img_path, 'rb') as f:
                    image = f.read()
            else:
                raise UserError('Thiếu hình ở buiding_unit_inherit/static/img/toanha.jpg')
            image_data =  tools.image_resize_image_big(base64.b64encode(image))
            r.image = image_data


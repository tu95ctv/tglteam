# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools
from odoo.modules import get_module_resource
import base64
from odoo.exceptions import UserError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.is_unit:
            self.image = self.product_id.image

    @api.onchange('relationship_owner_id')
    def _onchange_relationship_owner_id(self):
        if self.is_resident:
            self.image = self.relationship_owner_id.image

    
    # @api.model_create_multi
    # def create(self, vals_list):
    #     for vals in vals_list:
    #         if vals.get('is_unit') and not vals.get('image'):
    #             img_path = get_module_resource('buiding_management_inherit', 'static/img', 'toanha.jpg')
    #             if img_path:
    #                 with open(img_path, 'rb') as f:
    #                     image = f.read()
    #             else:
    #                 raise UserError('Thiếu hình ở buiding_management_inherit/static/img/toanha.jpg')
    #             image_data =  tools.image_resize_image_big(base64.b64encode(image))
    #             vals['image'] = image_data
    #     return super(ResPartner,self).create(vals_list)


    # @api.model_create_multi
    # def create(self, vals_list):
    #     for vals in vals_list:
    #         if vals.get('is_unit') and vals.get('product_id'):
    #             image_data =  self.env['product.product'].browse(vals.get('product_id')).image
    #             vals['image'] = image_data
    #     return super(ResPartner,self).create(vals_list)
    
    @api.multi 
    def update_avatar_image(self):
        for r in self:
            if r.is_unit:
                if r.product_id.image and not r.image:
                    r.image = r.product_id.image
                elif not r.image:
                    img_path = get_module_resource('buiding_management_inherit', 'static/img', 'toanha.jpg')
                    if img_path:
                        with open(img_path, 'rb') as f:
                            image = f.read()
                    else:
                        raise UserError('Thiếu hình ở buiding_management_inherit/static/img/toanha.jpg')
                    image_data =  tools.image_resize_image_big(base64.b64encode(image))
                    r.image = image_data
            elif r.is_resident:
                if r.relationship_owner_id.image and not r.image:
                    r.image = r.relationship_owner_id.image

    
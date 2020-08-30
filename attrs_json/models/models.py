# -*- coding: utf-8 -*-

from odoo import models, fields, api
import json
from odoo.addons import decimal_precision as dp

class Product(models.Model):
    _inherit = 'product.product'
    attribute_value_ids_json = fields.Char()
    attrs_jsonb_show = fields.Char(compute='_attrs_jsonb_show')
    pname = fields.Char(related='name', store=True)
    lst_price = fields.Float(
        'Sale Price', compute='_compute_product_lst_price', store=True,
        digits=dp.get_precision('Product Price'), inverse='_set_product_lst_price',
        help="The sale price is managed from the product template. Click on the 'Configure Variants' button to set the extra attribute prices.")
    # attrs_json = fields.Json()

    def _attrs_jsonb_show(self):
        for r in self:
            query = '''SELECT attrs_jsonb from product_product
            WHERE id = %s'''%(r.id)
            self.env.cr.execute(query)
            rs = self.env.cr.dictfetchall()
            if rs:
                rs = rs[0]['attrs_jsonb']
                r. attrs_jsonb_show = rs

    def thay_doi_attribute_value_ids(self,obj, vals):
        if 'attribute_value_ids' in vals:
            for r in obj:
                adict = {}
                for attr in r.attribute_value_ids:
                    attribute_id = attr.attribute_id.name
                    adict[attribute_id] = attr.id
                    # r.attribute_value_ids_json = adict
                    query = '''UPDATE product_product
                    SET attrs_jsonb = '%s'::jsonb
                    WHERE id = %s'''%(json.dumps(adict), r.id)
                    self.env.cr.execute(query)
                    # rs = self.env.cr.fetchall()
                    # print ('***rs***',rs)


    @api.model
    def create(self,vals):
        # self.clear_caches()
        rs = super(Product, self.sudo()).create(vals)
        self.thay_doi_attribute_value_ids(rs, vals)
        return rs

   
    @api.multi
    def write(self, vals):
        # self.clear_caches()
        rs = super(Product, self.sudo()).write(vals)
        self.thay_doi_attribute_value_ids(self, vals)
        return rs
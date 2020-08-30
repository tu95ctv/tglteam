# -*- coding: utf-8 -*-
from odoo import fields, models, api


class Base(models.AbstractModel):
    _inherit = 'base'

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        res = super(Base, self).search_read(domain=domain, fields=fields, offset=offset, limit=limit, order=order)
        depth_fields = self._context.get('depth_fields', {})
        ir_model_field = self.env['ir.model.fields']
        if depth_fields:
            for field_name, sub_fields in depth_fields.items():
                if field_name not in fields:
                    continue
                relation_field = ir_model_field.search(
                    [('ttype', 'in', ('one2many', 'many2many')),
                    ('model_id.model', '=', self._name),
                    ('name', '=', field_name)])
                if relation_field:
                    for item in res:
                        item[field_name] = self.env[relation_field.relation].with_context(depth_fields=False).search_read(
                            [('id', 'in', item[field_name])], sub_fields
                        )
        return res

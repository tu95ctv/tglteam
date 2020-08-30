# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.tools.safe_eval import safe_eval
from odoo.tools.image import image_data_uri

class MobileAPI(models.Model):
    _name = 'vidoo.mobile.api'

    @api.depends('api_field_ids')
    def _compute_api_fields_str(self):
        for record in self:
            record.api_fields_str = str(record.api_field_ids.mapped('name'))

    name = fields.Char('Name', default='Test API')
    endpoint = fields.Char(string='Custom Endpoint', required=True)
    route = fields.Char(compute='_compute_route', string='Custom Endpoint', readonly=True, store=True)
    model_id = fields.Many2one('ir.model', 'Model', required=True)
    model_name = fields.Char(related='model_id.model')
    api_domain = fields.Char('Domain', default='[]')

    api_field_ids = fields.Many2many(
        'ir.model.fields',
        'test_api_model_field_rel',
        'api_id',
        'field_id',
        string='Fields',
        domain="[('model_id', '=', model_id)]")

    api_fields_str = fields.Char('Fields name', compute='_compute_api_fields_str', readonly=False, store=True)

    api_offset = fields.Integer('Offset', default=0)
    api_limit = fields.Integer('Limit', default=10)
    api_order = fields.Char('Sort by', default='id')

    api_context = fields.Text('Context', default='{}')

    result = fields.Text('Result')

    @api.depends('endpoint')
    def _compute_route(self):
        for record in self:
            record.route = record.endpoint and "/api/public/%s" % record.endpoint.strip("/")

    def get_data(self):
        self.ensure_one()
        context = {
            'depth_fields': {
                'attribute_line_ids': ['attribute_id', 'value_ids'],
            }
        }
        ctx = safe_eval(self.api_context)
        datas = self.env[self.model_name].with_context(ctx).search_read(
            domain=safe_eval(self.api_domain),
            fields=safe_eval(self.api_fields_str),
            limit=self.api_limit,
            offset=self.api_offset,
            order=self.api_order)
        return datas

    def test_get_data(self):
        self.result = str(self.get_data())

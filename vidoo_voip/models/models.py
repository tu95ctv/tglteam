# -*- coding: utf-8 -*-

from odoo import models, fields, api

class VoiceIP(models.Model):
    _name = 'vidoo.voip'

    _inherit = ['mail.thread']
    caller_number = fields.Char('Số gọi', required=True)
    dial_number = fields.Char('Số nhận', required=True)
    start_time = fields.Datetime('Thời gian bắt đầu')
    duration = fields.Float('Thời lượng cuộc gọi')
    wait_time = fields.Float('Thời gian chờ')
    state = fields.Selection([('answered','Đã trả lời'), ('cancel','Từ chối'), ('no_answered','Chưa trả lời')],string='Trạng thái')
    type = fields.Selection([('out','Gọi ra'), ('in','Gọi vào'), ('internal','Nội bộ')],'Kiểu cuộc gọi')
    customer_id = fields.Many2one('res.partner','Khách hàng')
    product_ids = fields.Many2many('product.product','voip_product_rel','voip_id', 'product_id','Sản phẩm')
    address = fields.Char('Địa chỉ')
    sale_order_id = fields.Many2one('sale.order','Đơn hàng')
    record_file_link = fields.Char('Link file ghi âm')
    record_file_link_html = fields.Html(compute='_compute_record_file_link_html',string='File ghi âm')

    @api.depends('record_file_link')
    def _compute_record_file_link_html(self):
        for r in self:
            if r.record_file_link:
                r.record_file_link_html = '<p><a href="%s" class="btn btn-alpha" target="_blank">Link</a></p>'%r.record_file_link

    @api.multi
    def name_get(self):
        result = []
        for r in self:
            if r.caller_number and r.dial_number:
                name = 'Số gọi: %s, Số nhân:%s'%(r.caller_number, r.dial_number)
            else:
                name = 'New'
        result.append((r.id, name))
        return result




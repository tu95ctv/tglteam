# -*- coding: utf-8 -*-
from odoo import fields, models, tools, api
import odoo.addons.decimal_precision as dp

class InventoryReport(models.Model):
    _name = 'vio.inventory.report'
    _description = 'Báo cáo xuất nhập tồn'

    name = fields.Char(string="Tên", default='Báo cáo xuất nhập tồn')
    inventory_report_line_ids = fields.One2many('vio.inventory.report.line', 'inventory_report_id', string='Chi tiết')
    range_id = fields.Many2one('date.range', string='Chu kỳ')
    date_from = fields.Date(string='Từ ngày')
    date_to = fields.Date(string='Đến ngày')
    type_get_value = fields.Selection(selection=[
            ('product', 'Giá trên sản phẩm'),
            ('stock', 'Quy trình kho'),
            ('account', 'Bút toán'),
        ], string='Lấy giá trị theo', default='product')
    value = fields.Float(string='Giá trị kho', digits=dp.get_precision('Product Price'), readonly=True)
    warehouse_id = fields.Many2one('stock.warehouse', 'Kho hàng')
    user_id = fields.Many2one('res.users')

    @api.onchange('range_id')
    def _onchange_range_id(self):
        self.name = self.range_id.name
        self.date_from = self.range_id.date_start
        self.date_to = self.range_id.date_end

    def action_get_data_inventory_report_line(self):
        LineObj = self.env['vio.inventory.report.line']
        products = self.env['product.product'].search([('type', '=', 'product')])
        location_ids = []
        value = 0
        locations = self.env['stock.location'].search(['|', ('usage', '=', 'internal'), ('usage', '=', 'transit')])
        if self.warehouse_id:
            for location in locations:
                if location.get_warehouse().id == self.warehouse_id.id:
                    location_ids.append(location.id)
        else:
            location_ids = locations.ids

        domain_in = [('location_id', 'not in', location_ids),
                    ('location_dest_id', 'in', location_ids)]
        domain_out = [('location_id', 'in', location_ids),
                    ('location_dest_id', 'not in', location_ids)]

        move_in_ids = self.env['stock.move'].read_group(
                    [('state', '=', 'done'),
                    ('date', '>=', self.date_from),
                    ('date', '<=', self.date_to)] + domain_in,
                     fields=['product_id', 'product_qty'], groupby=['product_id'])

        move_out_ids = self.env['stock.move'].read_group([
                    ('state', '=', 'done'),
                    ('date', '>=', self.date_from),
                    ('date', '<=', self.date_to)] + domain_out,
                    fields=['product_id', 'product_qty'], groupby=['product_id'])

        for product in products:
            qty_opening = product.with_context(location_ids=location_ids, to_date=self.date_from).qty_available
            qty_closing = product.with_context(location_ids=location_ids, to_date=self.date_to).qty_available
            # qty_middling = product.with_context(location_ids=location_ids, from_date=self.date_from, to_date=self.date_to)
            line = LineObj.search([('inventory_report_id', '=', self.id), ('product_id', '=', product.id)], limit=1)
            if not line:
                line = LineObj.create({
                        'inventory_report_id': self.id,
                        'product_id': product.id,
                        'uom_id': product.uom_id.id,
                        'stock_opening': qty_opening,
                        'stock_value_opening': product.standard_price * qty_opening,
                        'stock_closing': qty_closing,
                        'stock_value_closing': product.standard_price * qty_closing
                    })
            value += product.standard_price * qty_closing
        self.value = value

        for move_in in move_in_ids:
            line = self.env['vio.inventory.report.line'].search([
                ('product_id', '=', move_in['product_id'][0]),
                ('inventory_report_id', '=', self.id)])
            product = self.env['product.product'].browse(move_in['product_id'][0])
            line.write({
                'stock_in': move_in['product_qty'],
                'stock_value_in': move_in['product_qty'] * product.standard_price
            })
        for move_out in move_out_ids:
            line = self.env['vio.inventory.report.line'].search([
                ('product_id', '=', move_out['product_id'][0]),
                ('inventory_report_id', '=', self.id),
            ])
            product = self.env['product.product'].browse(move_out['product_id'][0])
            line.write({
                'stock_out': move_out['product_qty'],
                'stock_value_out': move_out['product_qty'] * product.standard_price,
            })

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id)
    sum_stock_opening = fields.Float(string="Tổng Tồn đầu kỳ", digits=dp.get_precision('Product Unit of Measure'), compute='_compute_sum_stock_opening')
    sum_stock_value_opening = fields.Float(string='Tổng Giá trị tồn đầu kỳ', digits=dp.get_precision('Product Price'), compute='_compute_sum_stock_value_opening')
    sum_stock_in = fields.Float(string="Tổng Nhập trong kỳ", digits=dp.get_precision('Product Unit of Measure'), compute='_compute_sum_stock_in')
    sum_stock_value_in = fields.Float(string='Tổng Giá trị nhập trong kỳ', digits=dp.get_precision('Product Price'), compute='_compute_sum_stock_value_in')
    sum_stock_out = fields.Float(string="Tổng Xuất trong kỳ", digits=dp.get_precision('Product Unit of Measure'), compute='_compute_sum_stock_out')
    sum_stock_value_out = fields.Float(string='Tổng Giá trị xuất trong kỳ', digits=dp.get_precision('Product Price'), compute='_compute_sum_stock_value_out')
    sum_stock_closing = fields.Float(string="Tổng Tồn cuối kỳ", digits=dp.get_precision('Product Unit of Measure'), compute='_compute_sum_stock_closing')
    sum_stock_value_closing = fields.Float(string='Tổng Giá trị tồn cuối kỳ', digits=dp.get_precision('Product Price'), compute='_compute_sum_stock_value_closing')


    @api.depends('inventory_report_line_ids')
    def _compute_sum_stock_opening(self):
        for r in self:
            r.sum_stock_opening = sum(r.inventory_report_line_ids.mapped('stock_opening'))

    @api.depends('inventory_report_line_ids')
    def _compute_sum_stock_value_opening(self):
        for r in self:
            r.sum_stock_value_opening = sum(r.inventory_report_line_ids.mapped('stock_value_opening'))

    @api.depends('inventory_report_line_ids')
    def _compute_sum_stock_in(self):
        for r in self:
            r.sum_stock_in = sum(r.inventory_report_line_ids.mapped('stock_in'))

    @api.depends('inventory_report_line_ids')
    def _compute_sum_stock_value_in(self):
        for r in self:
            r.sum_stock_value_in = sum(r.inventory_report_line_ids.mapped('stock_value_in'))

    @api.depends('inventory_report_line_ids')
    def _compute_sum_stock_out(self):
        for r in self:
            r.sum_stock_out = sum(r.inventory_report_line_ids.mapped('stock_out'))
    
    @api.depends('inventory_report_line_ids')
    def _compute_sum_stock_value_out(self):
        for r in self:
            r.sum_stock_value_out = sum(r.inventory_report_line_ids.mapped('stock_value_out'))

    @api.depends('inventory_report_line_ids')
    def _compute_sum_stock_closing(self):
        for r in self:
            r.sum_stock_closing = sum(r.inventory_report_line_ids.mapped('stock_closing'))

    @api.depends('inventory_report_line_ids')
    def _compute_sum_stock_value_closing(self):
        for r in self:
            r.sum_stock_value_closing = sum(r.inventory_report_line_ids.mapped('stock_value_closing'))

    def display_address(self):
        return self.company_id.partner_id._display_address(without_company=True).replace('\n','')
    def display_warehouse(self):
        return ('Kho ' + self.warehouse_id.name) if self.warehouse_id.name else ''
class InventoryReportLine(models.Model):
    _name = 'vio.inventory.report.line'
    _description = 'Chi tiết xuất nhập tồn'

    inventory_report_id = fields.Many2one(string='Inventory report id', comodel_name='vio.inventory.report', ondelete='cascade')
    product_id = fields.Many2one(string='Sản phẩm', comodel_name='product.product')
    uom_id = fields.Many2one(string='Đơn vị', comodel_name='uom.uom')
    stock_opening = fields.Float(string="Tồn đầu kỳ", digits=dp.get_precision('Product Unit of Measure'))
    stock_value_opening = fields.Float(string='Giá trị tồn đầu kỳ', digits=dp.get_precision('Product Price'))
    stock_in = fields.Float(string="Nhập trong kỳ", digits=dp.get_precision('Product Unit of Measure'))
    stock_value_in = fields.Float(string='Giá trị nhập trong kỳ', digits=dp.get_precision('Product Price'))
    stock_out = fields.Float(string="Xuất trong kỳ", digits=dp.get_precision('Product Unit of Measure'))
    stock_value_out = fields.Float(string='Giá trị xuất trong kỳ', digits=dp.get_precision('Product Price'))
    stock_closing = fields.Float(string="Tồn cuối kỳ", digits=dp.get_precision('Product Unit of Measure'))
    stock_value_closing = fields.Float(string='Giá trị tồn cuối kỳ', digits=dp.get_precision('Product Price'))


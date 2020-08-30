# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockMove(models.Model):
    _inherit = 'stock.move'

    sale_price_unit = fields.Float(related='sale_line_id.price_unit', store=True)
    tax_id = fields.Many2many('account.tax','stock_move_tax_rel','stock_move_id','tax_id', related='sale_line_id.tax_id', store=True)
    price_subtotal = fields.Monetary(compute='_compute_all_amount', string='Subtotal', readonly=True, store=True,compute_sudo=True)
    price_tax = fields.Float(compute='_compute_all_amount', compute_sudo=True, string='Total Tax', readonly=True, store=True)
    price_total = fields.Monetary(compute='_compute_all_amount', compute_sudo=True, string='Total', readonly=True, store=True)
    discount = fields.Float(related='sale_line_id.discount', store=True)
    currency_id = fields.Many2one(related='sale_line_id.currency_id', store=True)
    discount_value = fields.Monetary(compute='_compute_all_amount', compute_sudo=True, string='Discount Value', readonly=True, store=True)
    sale_price_after_discount = fields.Float(compute='_compute_all_amount', store=True, string="sale_price_after_discount")
    @api.depends('quantity_done', 'discount', 'sale_price_unit', 'tax_id')
    def _compute_all_amount(self):
        for line in self:
            price = line.sale_price_unit * (1 - (line.discount or 0.0) / 100.0)
            line.sale_price_after_discount = price
            taxes = line.tax_id.compute_all(price, line.currency_id, line.quantity_done, product=line.product_id, partner=line.sale_line_id.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
                'discount_value': line.discount/100 * line.quantity_done * line.sale_price_unit
            })
    
    @api.depends('quantity_done', 'discount', 'sale_price_unit', 'tax_id')
    def _get_taxes(self):
        for line in self:
            price = line.sale_price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.currency_id, line.quantity_done, product=line.product_id, partner=line.sale_line_id.order_id.partner_shipping_id)
        return taxes['taxes']


class StockPicking(models.Model):
    _inherit = 'stock.picking'


    currency_id = fields.Many2one("res.currency", related='sale_id.currency_id', string="Currency", store=True)
    amount_untaxed = fields.Monetary(string='Untaxed Amount',
        store=True, readonly=True, compute='_compute_amount', compute_sudo=True)
    amount_tax = fields.Monetary(string='Tax',
        store=True, readonly=True, compute='_compute_amount', compute_sudo=True)
    amount_total = fields.Monetary(string='Total',
        store=True, readonly=True, compute='_compute_amount', compute_sudo=True)

    @api.depends('move_ids_without_package.price_subtotal', 'move_ids_without_package.price_tax')
    def _compute_amount(self):
        for r in self:
            r.amount_untaxed = sum(line.price_subtotal for line in r.move_ids_without_package)
            r.amount_tax  = sum(line.price_tax for line in r.move_ids_without_package)
            r.amount_total = r.amount_untaxed + r.amount_tax
    
    def _get_sum_tax_lines(self):
        for r in self:
            result_tax_lines = {}
            for line in r.move_ids_without_package:
                for taxline in line._get_taxes():
                    key = taxline['name']
                    result_tax_lines.setdefault(key, 0)
                    result_tax_lines[key] += taxline['amount']

            r.result_tax_lines = result_tax_lines





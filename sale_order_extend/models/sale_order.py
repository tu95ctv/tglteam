from odoo import api, models, fields
from odoo.addons import decimal_precision as dp
from odoo.tools.misc import formatLang, format_date


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def tgl_compute_product_str(self):
        template_line = '<div>{}</div>'
        for record in self:
            products_str = ''.join([template_line.format(line.with_context(with_name=1).line_str) for line in record.order_line])
            record.products_str = products_str

    @api.depends('invoice_ids', 'invoice_ids.amount_total')
    def _compute_invoice_total(self):
        for r in self:
            invoices = self.env['account.invoice'].search([('id', 'in', r.invoice_ids.ids), ('state', '!=', 'cancel')])
            r.invoice_total = sum(invoices.mapped('amount_total'))

    @api.depends('invoice_ids', 'invoice_ids.residual', 'invoice_ids.amount_total')
    def _compute_invoice_liabilities(self):
        for r in self:
            validate_invoices = self.env['account.invoice'].search([('id', 'in', r.invoice_ids.ids), ('state', '!=', 'cancel'), ('state', '!=', 'draft')])
            draft_invoices = self.env['account.invoice'].search([('id', 'in', r.invoice_ids.ids), ('state', '!=', 'cancel'), ('state', '=', 'draft')])
            r.invoice_liabilities = sum(validate_invoices.mapped('residual')) + sum(draft_invoices.mapped('amount_total'))

    @api.depends('invoice_total', 'invoice_liabilities')
    def _compute_invoice_paid(self):
        for r in self:
            r.invoice_paid = r.invoice_total - r.invoice_liabilities

    @api.depends('amount_total', 'invoice_paid')
    def _compute_sale_liabilities(self):
        for r in self:
            r.sale_liabilities = r.amount_total - r.invoice_paid

    products_str = fields.Html(string='Sản phẩm/dịch vụ', compute='tgl_compute_product_str')
    invoice_total = fields.Float(string='Tổng hóa đơn', compute='_compute_invoice_total', compute_sudo=True, store=True)
    invoice_liabilities = fields.Float(string='Phải thu', compute='_compute_invoice_liabilities', compute_sudo=True, store=True)
    invoice_paid = fields.Float(string='Đã trả', compute='_compute_invoice_paid', compute_sudo=True, store=True)
    sale_liabilities = fields.Float(string='Chưa thanh toán', compute='_compute_sale_liabilities', compute_sudo=True, store=True)
    qty_sum = fields.Float(string='Tổng SL', compute='_compute_qty_sum', store=True)
    qty_delivered = fields.Float(string='Số lượng đã giao', compute='_compute_qty_and_amount_delivered', store=True)
    delivered_amount = fields.Float(string='Giá trị đã giao', compute='_compute_qty_and_amount_delivered', store=True)

    @api.depends('order_line')
    def _compute_qty_sum(self):
        for r in self:
            r.qty_sum = sum(r.order_line.mapped('product_uom_qty'))

    


    @api.depends('order_line.qty_delivered')
    def _compute_qty_and_amount_delivered(self):
        for r in self:
            # qty_delivered = 0
            # delivered_amount = 0
            # for l in r.order_line:
            #     delivered_amount += l.qty_delivered * l.price_unit
            #     qty_delivered += l.qty_delivered
            # r.delivered_amount = delivered_amount
            # r.qty_delivered = qty_delivered
            qty_delivered = 0
            price_total = 0
            for line in r.order_line:
                qty_delivered += line.qty_delivered
                price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                line.sale_price_after_discount = price
                taxes = line.tax_id.compute_all(price, line.currency_id, line.qty_delivered, 
                    product=line.product_id, partner=r.partner_shipping_id)
                price_total = price_total + taxes['total_included']
            r.delivered_amount = price_total
            r.qty_delivered = qty_delivered
                # {
                #     'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                #     'discount_value': line.sale_price_unit * line.quantity_done * line.discount / 100.0,
                #     'price_total': taxes['total_included'],
                #     'price_subtotal': taxes['total_excluded'],
                # }


    @api.depends('order_line.price_total')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
            order.update({
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax,
                'amount_total': amount_untaxed + amount_tax,
            })

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    def tgl_compute_line_str(self):
        template_line = '{} x {} = {}'
        template_discount_fixed = '{} x ({} - {}) = {}'
        template_discount_percent = '{} x {} (-{}%) = {}'
        for line in self:
            line_str = ''
            if self._context.get('with_name'):
                line_str = '+ ' + line.name + ': '
            if line.discount_fixed:
                line_str += template_discount_fixed.format(
                    formatLang(self.env, line.product_uom_qty, digits=0),
                    formatLang(self.env, line.price_unit, digits=0),
                    formatLang(self.env, line.discount_fixed, digits=0),
                    formatLang(self.env, line.price_subtotal, digits=0),
                )
            elif line.discount:
                line_str += template_discount_percent.format(
                    formatLang(self.env, line.product_uom_qty, digits=0),
                    formatLang(self.env, line.price_unit, digits=0),
                    formatLang(self.env, line.discount, digits=0),
                    formatLang(self.env, line.price_subtotal, digits=0),
                )
            else:
                line_str += template_line.format(
                    formatLang(self.env, line.product_uom_qty, digits=0),
                    formatLang(self.env, line.price_unit, digits=0),
                    formatLang(self.env, line.price_subtotal, digits=0),
                )
            line.line_str = line_str

    line_str = fields.Text('Products str', compute='tgl_compute_line_str')
    discount_fixed = fields.Float(string="Giảm giá", digits=dp.get_precision('Product Price'))

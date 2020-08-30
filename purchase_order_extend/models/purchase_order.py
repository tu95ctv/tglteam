from odoo import api, models, fields
from odoo.addons import decimal_precision as dp
from odoo.tools.misc import formatLang, format_date


class SaleOrder(models.Model):
    _inherit = 'purchase.order'

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

class SaleOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.multi
    def tgl_compute_line_str(self):
        template_line = '{} x {} = {}'
        template_discount_fixed = '{} x ({} - {}) = {}'
        template_discount_percent = '{} x {} (-{}%) = {}'
        for line in self:
            line_str = ''
            if self._context.get('with_name'):
                line_str = '+ ' + line.name + ': '
            if getattr(line, 'discount_fixed', False):
                line_str += template_discount_fixed.format(
                    formatLang(self.env, line.product_uom_qty, digits=0),
                    formatLang(self.env, line.price_unit, digits=0),
                    formatLang(self.env, line.discount_fixed, digits=0),
                    formatLang(self.env, line.price_subtotal, digits=0),
                )
            elif getattr(line, 'discount', False):
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

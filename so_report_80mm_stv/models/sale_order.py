from odoo import fields, models, api, tools, _
from odoo.tools.misc import formatLang

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # @api.multi
    # def get_taxes_values(self):
    #     tax_grouped = {}
    #     round_curr = self.currency_id.round
    #     for line in self.invoice_line_ids:
    #         if not line.account_id:
    #             continue
    #         price_unit = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
    #         taxes = line.invoice_line_tax_ids.compute_all(price_unit, self.currency_id, line.quantity, line.product_id, self.partner_id)['taxes']
    #         for tax in taxes:
    #             val = self._prepare_tax_line_vals(line, tax)
    #             key = self.env['account.tax'].browse(tax['id']).get_grouping_key(val)

    #             if key not in tax_grouped:
    #                 tax_grouped[key] = val
    #                 tax_grouped[key]['base'] = round_curr(val['base'])
    #             else:
    #                 tax_grouped[key]['amount'] += val['amount']
    #                 tax_grouped[key]['base'] += round_curr(val['base'])
    #     return tax_grouped

    def get_taxes_value(self):
        res = {}
        for line in self.order_line:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.currency_id, line.product_uom_qty, product=line.product_id, partner=self.partner_shipping_id)
            for tax in taxes['taxes']:
                res.setdefault(tax['name'], 0)
                res[tax['name']] += tax['amount']
        return res

    @property
    def amount_untaxted_after_discount(self):
        amount = 0
        for line in self.order_line:
            amount += line.price_unit * line.product_uom_qty
        return amount
        
    @property
    def amount_discount(self):
        amount = 0
        for line in self.order_line:
            amount += line.price_unit * line.product_uom_qty * line.discount/100.0
        return amount

            

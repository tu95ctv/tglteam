# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountingCommonPartnerReport(models.TransientModel):
    _name = 'account.common.partner.report'
    _description = 'Account Common Partner Report'
    _inherit = "account.common.report"

    result_selection = fields.Selection([('customer', 'Phải thu'),
                                         ('supplier', 'Phải trả'),
                                         ('customer_supplier', 'Phải thu và phải trả')
                                         ], string="Loại", required=True, default='customer')

    def pre_print_report(self, data):
        data['form'].update(self.read(['result_selection'])[0])
        return data

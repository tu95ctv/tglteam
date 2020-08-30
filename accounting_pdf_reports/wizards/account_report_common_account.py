# -*- coding: utf-8 -*-

from odoo import api, fields, models


class AccountCommonAccountReport(models.TransientModel):
    _name = 'account.common.account.report'
    _description = 'Account Common Account Report'
    _inherit = "account.common.report"

    display_account = fields.Selection([('all', 'Tất cả'), ('movement', 'Có phát sinh'),
                                        ('not_zero', 'Có số dư khác 0'), ],
                                       string='Hiển thị tài khoản', required=True, default='movement')

    @api.multi
    def pre_print_report(self, data):
        data['form'].update(self.read(['display_account'])[0])
        return data

# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountTaxReport(models.TransientModel):
    _inherit = 'account.tax.report'
    model_report_name = 'report.accounting_pdf_reports.report_tax'

    @property
    def get_py3o_accounts_lines(self):
        res = self.check_report()
        context = dict(res['context'], active_model=self._name, active_id=self.id)
        data = res.get('data', {})
        get_report_values_rsul = self.env[self.model_report_name].with_context(context).\
            _get_report_values(self, data)
        return [get_report_values_rsul]

# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountTaxReport(models.TransientModel):
    _inherit = "account.common.report"
    _name = 'account.tax.report'
    _description = 'Tax Report'

    def _print_report(self, data):
        return self.env.ref('accounting_pdf_reports.action_report_account_tax').report_action(self, data=data)

    name = fields.Char(default='Tax Reports')
    result_html = fields.Html('Result', readonly=False)

    def tgl_get_data(self):
        res = self.check_report()
        context = dict(res['context'], active_model=self._name, active_id=self.id)
        self.result_html = self.env.ref('accounting_pdf_reports.action_report_account_tax').with_context(context).render_qweb_html(None, data=res.get('data', {}))[0]
        return False
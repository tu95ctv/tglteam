# -*- coding: utf-8 -*-

from odoo import fields, models, _


class AccountPartnerLedger(models.TransientModel):
    _inherit = "account.common.partner.report"
    _name = "account.report.partner.ledger"
    _description = "Account Partner Ledger"

    amount_currency = fields.Boolean("Hiển thị tiền tệ",
                                     help="It adds the currency column on report if the "
                                          "currency differs from the company currency.")
    reconciled = fields.Boolean('Đã đối soát')

    def _print_report(self, data):
        data = self.pre_print_report(data)
        data['form'].update({'reconciled': self.reconciled, 'amount_currency': self.amount_currency})
        return self.env.ref('accounting_pdf_reports.action_report_partnerledger').report_action(self, data=data)

    name = fields.Char(default='Partner Ledger')
    result_html = fields.Html('Result', readonly=False)

    def tgl_get_data(self):
        res = self.check_report()
        context = dict(res['context'], active_model=self._name, active_id=self.id)
        self.result_html = self.env.ref('accounting_pdf_reports.action_report_partnerledger').with_context(context).render_qweb_html(None, data=res.get('data', {}))[0]
        return False
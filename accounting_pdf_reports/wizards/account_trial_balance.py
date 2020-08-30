# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountBalanceReport(models.TransientModel):
    _inherit = "account.common.account.report"
    _name = 'account.balance.report'
    _description = 'Trial Balance Report'

    journal_ids = fields.Many2many('account.journal', 'account_balance_report_journal_rel', 'account_id', 'journal_id', string='Sổ nhật ký', required=True, default=[])

    def _print_report(self, data):
        data = self.pre_print_report(data)
        records = self.env[data['model']].browse(data.get('ids', []))
        return self.env.ref('accounting_pdf_reports.action_report_trial_balance').report_action(records, data=data)

    display_account = fields.Selection(default='all')
    name = fields.Char(default='Trial Balance')
    result_html = fields.Html('Result', readonly=False)

    def tgl_get_data(self):
        res = self.check_report()
        context = dict(res['context'], active_model=self._name, active_id=self.id)
        self.result_html = self.env.ref('accounting_pdf_reports.action_report_trial_balance').with_context(context).render_qweb_html(None, data=res.get('data', {}))[0]
        return False

# -*- coding: utf-8 -*-

from odoo import fields, models, _
from odoo.exceptions import UserError

# TGL
class AccountCommonReport(models.TransientModel):
    _inherit = "account.common.report"

    company_id = fields.Many2one(string='Công ty')
    journal_ids = fields.Many2many(string='Sổ nhật ký')
    date_from = fields.Date(string='Ngày bắt đầu')
    date_to = fields.Date(string='Ngày kế thúc')
    target_move = fields.Selection([('posted', 'Đã vào sổ'), ('all', 'Tất cả')], string='Lọc bút toán', required=True, default='posted')
# END: TGL

class AccountReportGeneralLedger(models.TransientModel):
    _inherit = "account.common.account.report"
    _name = "account.report.general.ledger"
    _description = "General Ledger Report"

    initial_balance = fields.Boolean(string='Bao gồm số dư đầu kỳ',
                                    help='If you selected date, this field allow you to add a row to display the amount of debit/credit/balance that precedes the filter you\'ve set.')
    sortby = fields.Selection([('sort_date', 'Ngày'), ('sort_journal_partner', 'Đối tác')], string='Sắp xếp theo', required=True, default='sort_date')
    journal_ids = fields.Many2many('account.journal', 'account_report_general_ledger_journal_rel', 'account_id', 'journal_id', string='Sổ nhật ký', required=True)

    def _print_report(self, data):
        data = self.pre_print_report(data)
        data['form'].update(self.read(['initial_balance', 'sortby'])[0])
        if data['form'].get('initial_balance') and not data['form'].get('date_from'):
            raise UserError(_("You must define a Start Date"))
        records = self.env[data['model']].browse(data.get('ids', []))
        return self.env.ref('accounting_pdf_reports.action_report_general_ledger').with_context(landscape=True).report_action(records, data=data)

    name = fields.Char(default='General Ledger')
    result_html = fields.Html('Result', readonly=False)

    def tgl_get_data(self):
        res = self.check_report()
        context = dict(res['context'], active_model=self._name, active_id=self.id)
        self.result_html = self.env.ref('accounting_pdf_reports.action_report_general_ledger').with_context(context).render_qweb_html(None, data=res.get('data', {}))[0]
        return False
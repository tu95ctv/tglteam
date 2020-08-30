# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountPrintJournal(models.TransientModel):
    _inherit = "account.common.journal.report"
    _name = "account.print.journal"
    _description = "Account Print Journal"

    sort_selection = fields.Selection([('date', 'Ngày'), ('move_name', 'Số bút toán'), ], 'Sắp xếp theo', required=True, default='move_name')
    journal_ids = fields.Many2many('account.journal', string='Sổ nhật ký', required=True, default=lambda self: self.env['account.journal'].search([('type', 'in', ['sale', 'purchase'])]))

    name = fields.Char(default='Journals Audit')
    result_html = fields.Html('Result', readonly=False)

    def tgl_get_data(self):
        res = self.check_report()
        context = dict(res['context'], active_model=self._name, active_id=self.id)
        self.result_html = self.env.ref('accounting_pdf_reports.action_report_journal').with_context(context).render_qweb_html(None, data=res.get('data', {}))[0]
        return False

    def _print_report(self, data):
        data = self.pre_print_report(data)
        data['form'].update({'sort_selection': self.sort_selection})
        return self.env.ref('accounting_pdf_reports.action_report_journal').with_context(landscape=True).report_action(self, data=data)

# -*- coding: utf-8 -*-

import time
from odoo import api, models, _
from odoo.exceptions import UserError

        

class AccountReportGeneralLedger(models.TransientModel):
    _inherit = "account.report.general.ledger"
    model_report_name = 'report.accounting_pdf_reports.report_generalledger'
    def get_py3o_accounts_lines(self):
        res = self.check_report()
        context = dict(res['context'], active_model=self._name, active_id=self.id)
        data = res.get('data', {})
        get_report_values_rsul = self.env[self.model_report_name].with_context(context).\
            _get_report_values(self, data)
        return get_report_values_rsul['Accounts']



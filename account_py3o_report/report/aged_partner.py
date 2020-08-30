# -*- coding: utf-8 -*-

import time
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountAgedTrialBalance(models.TransientModel):
    _inherit = 'account.aged.trial.balance'
    model_report_name = 'report.accounting_pdf_reports.report_agedpartnerbalance'

    @property
    def get_py3o_accounts_lines(self):
        res = self.check_report()
        context = dict(res['context'], active_model=self._name, active_id=self.id)
        data = res.get('data', {})
        get_report_values_rsul = self.env[self.model_report_name].with_context(context).\
            _get_report_values(self, data)
        return [get_report_values_rsul]

    
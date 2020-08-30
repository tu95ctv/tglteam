# -*- coding: utf-8 -*-

from odoo import fields, models, _


class AccountPartnerLedger(models.TransientModel):
    _inherit = "account.report.partner.ledger"
    model_report_name = 'report.accounting_pdf_reports.report_partnerledger'
  
    @property
    def get_py3o_accounts_lines(self):
        res = self.check_report()
        context = dict(res['context'], active_model=self._name, active_id=self.id)
        data = res.get('data', {})
        get_report_values_rsul = self.env[self.model_report_name].with_context(context).\
            _get_report_values(self, data)
        return [get_report_values_rsul]

    

    
        



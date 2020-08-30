# -*- coding: utf-8 -*-
from odoo import models, fields, api

class View(models.Model):
    _inherit = "ir.ui.view"

    is_banner_template = fields.Boolean()
    review_html = fields.Html(compute='_compute_review_html')
    def _compute_review_html(self):
        for r in self:
            if self._context.get('ui_view_in_web_banner'):
                template_id = r
                summary_report_config_context = self._context.get('summary_report_config')
                if summary_report_config_context and summary_report_config_context != True:
                    try:
                        summary_report_config = self.env['summary.report.config'].browse(int(summary_report_config_context))
                    except:
                        summary_report_config = self.env['summary.report.config']
                        
                else:
                    summary_report_config = self.env['summary.report.config']
                table_html = template_id.render({
                    'config': summary_report_config
                })
                u_table_html = table_html.decode("utf-8") 
                review_html = u_table_html.replace('col-xl-3 col-sm-6 col-12','').replace('col-xl-6 col-md-12','')
                r.review_html = review_html

    


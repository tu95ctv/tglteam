# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class OnboardingController(http.Controller):

    @http.route('/sale_quotation_onboarding_panel_overwrite/<string:res_model>', auth='user', type='json')
    def sale_quotation_onboarding(self, **kw):
        """ Returns the `banner` for the sale onboarding panel.
            It can be empty if the user has closed it or if he doesn't have
            the permission to see it. """
        res_model = kw['res_model']
        company = request.env.user.company_id
        if not request.env.user._is_admin() or \
           company.sale_quotation_onboarding_state == 'closed':
            return {}
        configs = request.env['summary.report.config'].search([('model_id.model','=', res_model)], order="priority asc")
        return {
            'html': request.env.ref('sale_order_summary.sale_quotation_onboarding_panel_overwrite').render({
                'configs':configs,
                'company': company,
                'state': company.get_and_update_sale_quotation_onboarding_state(),
            })
        }

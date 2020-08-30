# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    template_view_id = fields.Many2one('ir.ui.view')


    # @api.model
    # def get_values(self):
    #     res = super(ResConfigSettings, self).get_values()
    #     res.update(
    #         expense_alias_prefix=self.env.ref('hr_expense.mail_alias_expense').alias_name,
    #     )
    #     return res

    # @api.multi
    # def set_values(self):
    #     super(ResConfigSettings, self).set_values()
    #     self.env.ref('hr_expense.mail_alias_expense').write({'alias_name': self.expense_alias_prefix})


    def set_values(self):
        super(ResConfigSettings, self).set_values()
        # if self.default_invoice_policy != 'order':
        self.env['ir.config_parameter'].set_param('sale.template_view_id', self.template_view_id.id)

    # @api.model
    # def get_values(self):
    #     res = super(ResConfigSettings, self).get_values()
    #     get_param = self.env['ir.config_parameter'].sudo().get_param
    #     res.update(
    #         server_uri="%s/google_account/authentication" % get_param('web.base.url', default="http://yourcompany.odoo.com"),
    #     )
    #     return res

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        Params = self.env['ir.config_parameter'].sudo()
        value = int(Params.get_param('sale.template_view_id', False))
        print ("Params.get_param('sale.template_view_id', False)", Params.get_param('sale.template_view_id', False))
        res.update({
            'template_view_id': value,
        })
        return res
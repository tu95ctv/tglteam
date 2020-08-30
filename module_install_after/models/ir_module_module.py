# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class Module(models.Model):
    _inherit = "ir.module.module"

    def return_this_module_action(self):
        form_view = self.env.ref('base.module_form')
        return {
            'name': _('ir.module.module'),
            'res_model': 'ir.module.module',
            'res_id': self.id,
            'views': [(form_view.id, 'form'),],
            'type': 'ir.actions.act_window',
            # 'target': 'inline'
            'target': 'current'
            
        }
        
    def button_immediate_install(self):
        super(Module,self).button_immediate_install()
        return self.return_this_module_action()

    def button_immediate_upgrade(self):
        super(Module,self).button_immediate_install()
        return self.return_this_module_action()











    


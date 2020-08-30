# -*- coding: utf-8 -*-
from odoo import fields, models, tools, api
import odoo.addons.decimal_precision as dp

class InventoryReport(models.Model):
    _inherit = 'vio.inventory.report'

    @api.multi
    def export_to_excel(self):
        action = self.env.ref('inventory_report_py3o.vio_inventory_report').read()[0]
        return action

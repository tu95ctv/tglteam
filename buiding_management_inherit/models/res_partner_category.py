from odoo import models, fields, api, tools
from odoo.modules import get_module_resource
import base64
from odoo.exceptions import UserError

class ResPartner(models.Model):
    _inherit = 'res.partner.category'

    image = fields.Binary()
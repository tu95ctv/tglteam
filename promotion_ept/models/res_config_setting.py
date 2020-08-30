from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ResConfiguration(models.TransientModel):
    _inherit = 'res.config.settings'
    
    
    promotion_product_id = fields.Many2one(
        'product.product',
        'Promotion Product',
        domain="[('is_promo_product', '=', True)]",context="{'default_is_promo_product':1,'default_type':'service'}",
        help='Default product used for promotion apply in sale order')
    
    promotion_product_category_id = fields.Many2one(
        'product.category',
        'Promotion Product Category',
        help='Default product used for promotion apply in sale order')
    
    group_promotion_product=fields.Boolean("Create Promotion Product",implied_group='promotion_ept.group_promotion_product',group="promotion_ept.group_promotion_manager")
    
    group_promo_product_show=fields.Boolean("Show Promotion Product",implied_group='promotion_ept.group_promotion_product_show',group="promotion_ept.group_promotion_manager")
    
    @api.model
    def get_values(self):
        res = super(ResConfiguration, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        res.update(
            promotion_product_id=int(ICPSudo.get_param('sale.promotion_product_id', default=False)),
            promotion_product_category_id=int(ICPSudo.get_param('sale.promotion_product_category_id', default=False)),
        )
        return res
    
    @api.multi
    def set_values(self):
        super(ResConfiguration, self).set_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        ICPSudo.set_param("sale.promotion_product_id", self.promotion_product_id.id)
        ICPSudo.set_param("sale.promotion_product_category_id", self.promotion_product_category_id.id)
    
    @api.constrains('promotion_product_id','promotion_product_category_id')
    def _check_setting_validation(self):
        for record in self:
            if record.promotion_product_id.categ_id!=record.promotion_product_category_id:
                raise ValidationError(_("Promotion Product's category sould be match with promotion product category"))
            
    @api.onchange('promotion_product_id')
    def _onchange_group_discount_per_so_line_promotion(self):
        if self.promotion_product_id and not self.group_discount_per_so_line:
            self.update({
                'group_discount_per_so_line': True,
            })
            
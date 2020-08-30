# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    # App information

    'name': 'Manage Sale Promotions in Odoo',
    'category': 'Sales',
    'version': '12.0.2.0',
    'summary': 'Delight your customers and boost your sales by offering attractive coupons and promotional offers using Odoo Promotions',
    'license': 'OPL-1',

    # Dependencies
        'depends': ['sale_management'],

    # Views
        'data': [
            'wizard/promotion_extend_wizard.xml',
            'report/promotion_report_template.xml',
            'report/promotion_barcode_report.xml',
            'views/promotion_coupon.xml',
            'views/promotion_view.xml',
            'security/promotion_security.xml',
            'views/product.xml',
            'views/sale_order.xml',
            'data/email_template.xml',
            'views/sequence.xml',
            'views/res_config_setting.xml',
            #'data/promotion_demo.xml',

            # Security

            'security/ir.model.access.csv', ],

    # Author

    'author': 'Emipro Technologies Pvt. Ltd.',
    'website': 'http://www.emiprotechnologies.com',
    'maintainer': 'Emipro Technologies Pvt. Ltd.',

    # Odoo Store Specific

    'images': ['static/description/module_image.jpg'],


    # Technical

    'installable': True,
    'application': False,
    'auto_install': False,
    'live_test_url': 'https://www.emiprotechnologies.com/free-trial?app=promotion-ept&version=12&edition=enterprise',
    'price': '149',
    'currency': 'EUR',

}

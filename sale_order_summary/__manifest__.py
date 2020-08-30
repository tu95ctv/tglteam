# -*- coding: utf-8 -*-
{
    'name': "sale order summary",

    'summary': """
        Tình trạng thanh toán đơn hàng: tổng hóa đơn, đã trả, còn lại""",

    'description': """
        Tình trạng thanh toán đơn hàng: tổng hóa đơn, đã trả, còn lại
        Ở onboarding
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale'],

    # always loaded
    'data': [
        #security
        'security/security.xml',
        'security/ir.model.access.csv',
        #view
        'views/assets.xml',
        'views/sale_order_view.xml',
        'views/summary_report_config_view.xml',
        'views/summary_report_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
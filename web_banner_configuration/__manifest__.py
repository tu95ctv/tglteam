# -*- coding: utf-8 -*-
{
    "name": "Banner configuration",
    "summary": "Hỗ trợ thiết lập các chỉ số báo cáo",
    "version": "12.0.1.0.0",
    "category": "tools",
    "website": "https://trinhgialac.com",
    "author": "Trình Gia Lạc",
    "license": "AGPL-3",
    "depends": [
        "sale",
    ],
    "data": [
        #security
        "security/security.xml",
        "security/ir.model.access.csv",
        #view
        "views/assets.xml",
        "views/sale_order_view.xml",
        "views/summary_report_config_view.xml",
        "views/summary_report_templates.xml",
        "views/out_template_xl3.xml",
        "views/out_template_xl6.xml",
        "views/ir_ui_view.xml",
    ],
    "application": False,
    "installable": True,
}

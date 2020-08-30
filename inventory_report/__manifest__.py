# -*- coding: utf-8 -*-
{
    "name": "Inventory Report",
    "summary": "Báo cáo xuất nhập tồn",
    "version": "12.0.1.0.1",
    "category": "stock",
    "website": "",
    "author": "TGL team",
    "license": "AGPL-3",
    "depends": [
        "stock", "date_range"
    ],
    "data": [
        'security/ir.model.access.csv',
        'views/inventory_report.xml'
    ],
    "images": ["static/description/icon.png"],
    "application": False,
    "installable": True,
}

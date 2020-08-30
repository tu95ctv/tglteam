# -*- coding: utf-8 -*-
{
    "name": "Inventory Report XLS",
    "summary": "Bản in Excel cho     báo cáo xuất nhập tồn",
    "version": "12.0.1.0.1",
    "category": "stock",
    "website": "https://trinhgialac.com",
    "author": "TGL team",
    "license": "AGPL-3",
    "depends": [
        "report_py3o", "inventory_report"
    ],
    "data": [
        "report/inventory_report_py3o.xml",
        "views/inventory_report.xml",
    ],
    "images": ["static/description/icon.png"],
    "application": False,
    "installable": True,
}

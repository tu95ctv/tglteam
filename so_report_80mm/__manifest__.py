# -*- coding: utf-8 -*-
{
    'name': 'so_report_80mm',
    'summary': 'Bản in 80mm trên SO dựa theo số lượng giao',
    'description': """
        Bản in 80mm trên SO dựa theo số lượng giao
    """,
    'version': '12.0.1.0.4',
    "sequence": 5,
    "version": "12.0.1.0.1",
    "category": "sale",
    "website": "https://itc-group.vn/",
    "author": "ITC Group",
    "license": "AGPL-3",
    'depends': ['sale_stock'],
    'data': [
        'report/paper_format.xml',
        'report/so_report_80mm.xml',
        'views/warehouse_view.xml',
        'views/assets.xml',
    ],
}

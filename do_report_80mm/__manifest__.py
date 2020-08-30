# -*- coding: utf-8 -*-
{
    'name': 'do_report_80mm',
    'version': '12.0.1.0.4',
    "sequence": 5,
    'category': 'stock',
    "website": "https://itc-group.vn/",
    "author": "ITC Group",
    "license": "AGPL-3",
    'summary': 'Bản in 80mm phiếu soát hàng hoặc phiếu giao hàng',
    'description': """
        Bản in 80mm phiếu soát hàng hoặc phiếu giao hàng
    """,
    'depends': ['sale_stock'],
    'data': [
        'report/paper_format.xml',
        'report/do.xml',
        # 'views/warehouse_view.xml',
        # 'views/stock_picking_view.xml',
        'views/assets.xml',

    ],
    "application": False,
    "installable": True,
}
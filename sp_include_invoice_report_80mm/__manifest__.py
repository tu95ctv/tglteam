# -*- coding: utf-8 -*-
{
    'name': 'sp_include_invoice_report_80mm',
    'version': '12.0.1.0.4',
    "sequence": 5,
    'category': 'stock,sale,account',
    "website": "https://itc-group.vn/",
    "author": "ITC Group",
    "license": "AGPL-3",
    'summary': 'Bản in 80mm phiếu giao hàng kiêm hóa đơn',
    'description': """
        Bản in 80mm phiếu giao hàng kiêm hóa đơn
    """,
    'depends': ['sale_stock'],
    'data': [
        'report/paper_format.xml',
        'report/stock_picking_invoice_report.xml',
        'views/warehouse_view.xml',
        'views/stock_picking_view.xml',
        'views/assets.xml',
        

    ],
    "application": False,
    "installable": True,
}

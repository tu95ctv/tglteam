# -*- coding: utf-8 -*-
{
    'name': "Sales Orders Extend",
    'version': '12.01.0.1',
    'category': 'sale',
    'summary': "Bổ sung thêm thông tin trên Đơn hàng",
    'author': 'Trình Gia Lạc',
    'website': 'https://trinhgialac.com',
    "depends": [
        'sale_stock',
    ],
    "data": [
        'views/sale_order_view.xml',
    ],
    "application": False,
    "installable": True,
}

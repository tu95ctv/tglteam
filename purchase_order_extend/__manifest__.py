# -*- coding: utf-8 -*-
{
    'name': "Purchase Orders Extend",
    'version': '12.01.0.1',
    'category': 'purchase',
    'summary': "Bổ sung thêm thông tin trên phiếu mua hàng",
     "description":"""
        Thêm trường sản phẩm dịch vụ: liệt kê các sản phẩm kèm theo đơn giá, số lượng, giảm giá, thành tiền trước thuế
        Thêm các trường: Tổng hóa đơn, phải thu, đã trả, chưa thanh toán
    """,
    "author": "ITC Group",
    "license": "AGPL-3",
    "website": "https://itc-group.vn/",
    "depends": [
        'purchase',
    ],
    "data": [
        'views/purchase_order_view.xml',
    ],
    "application": False,
    "installable": True,
}

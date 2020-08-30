# -*- coding: utf-8 -*-
{
    "name": "API for mobile apps",
    "summary": "API for mobile apps",
    "version": "12.0.1.0.1",
    "description": """

        Cấu trúc hiển thị cho mobile

        Mở rộng search_read cho phép truy vấn nhiều hơn 1 cấp dữ liệu

    """,
    "category": "web",
    "author": "Trình Gia Lạc",
    "website": "https://trinhgialac.com",
    "depends": ["product", "product_pricelist_uom", "product_brand"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/product_view.xml",
        "views/ecommerce_view.xml",
        "views/mobile_api_view.xml",
        "views/menu_view.xml",
    ],
    "application": False,
    "installable": True,
}

# -*- coding: utf-8 -*-
{
    "name": "product_info_extend",
    "summary": "Khối lượng theo Gam, Thể tích theo ml",
    "description":"""Khối lượng theo Gam, khi thay đổi thì tính lại trường Khối lượng theo Kg (1 kg = 1000 g)
    Thể tích theo ml, khi thay đổi thì tính lại trường thể tích theo ml ( 1 mét khối = 1 triệu ml)
    """,
    "version": "12.0.1.0.1",
    "license": "AGPL-3",
    "category": "account",
    "website": "https://itc-group.vn/",
    "author": "ITC Group",
    "depends": ["base", "product"],
    "data": [
        # "security/ir.model.access.csv",
        "views/product_template.xml",
    ],
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "application": False,
    "installable": True,
    
}
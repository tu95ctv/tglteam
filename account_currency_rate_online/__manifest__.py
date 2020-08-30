# -*- coding: utf-8 -*-
{
    "name": "Online currency rate",
    "summary": "Lấy tỉ giá online từ Vietcombank",
    "description":"""
        Thu thập dữ liệu online cho tỉ giá từ trang web
        https://portal.vietcombank.com.vn/Usercontrols/TVPortal.TyGia/pXML.aspx
    """,
    
    "version": "12.0.1.0.1",
    "category": "account",
    "website": "https://itc-group.vn/",
    "author": "ITC Group",
    "license": "AGPL-3",
    "depends": ["tgl_currency_digits_extend"],
    "data": [
        "security/ir.model.access.csv",
        "data/fetch_all_rate_cron.xml",
        "data/fetch_single_rate_actions_server.xml",
        "views/res_currency_rate.xml"
    ],
    'external_dependencies': {
        'python': ['ssl'],
        'bin': [],
    },
    "application": False,
    "installable": True,
    
}
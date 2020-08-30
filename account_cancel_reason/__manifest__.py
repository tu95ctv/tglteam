# -*- coding: utf-8 -*-
{
    "name": "Payment, Invoice Cancel Reason",
    "summary": "Nhập lý do và tài liệu thì mới được xóa payment, invoice",
    "description":"",
    "version": "12.0.1.0.1",
    "license": "AGPL-3",
    "category": "account",
    "website": "https://itc-group.vn/",
    "author": "ITC Group",
    "depends": ["base", "account_cancel"],
    "data": [
        "security/ir.model.access.csv",
        "views/account_invoice.xml",
        "views/account_cancel_reason_wizard.xml",
    ],
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "application": False,
    "installable": True,
    
}
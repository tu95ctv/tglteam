# -*- coding: utf-8 -*-
{
    "name": "hr_document_template",
    "summary": "63 biểu mẫu hành chính",
    "description":"",
    "version": "12.0.1.0.1",
    "license": "AGPL-3",
    "category": "account",
    "website": "https://itc-group.vn/",
    "author": "ITC Group",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "data/bieu_mau_data.xml",
        "views/document_template.xml",
    ],
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "application": False,
    "installable": True,
    
}
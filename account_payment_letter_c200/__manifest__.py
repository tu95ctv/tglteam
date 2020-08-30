# -*- coding: utf-8 -*-
# module template
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'account_payment_letter_c200',
    "summary": "account_payment_letter_c200",
    "description":"",
    "version": "12.0.1.0.1",
    "category": "stock",
    "website": "https://itc-group.vn/",
    "author": "ITC Group",
    "license": "AGPL-3",
    'depends': ['base','account'
                ],
    'data': [
            'report/payment_report_c200_template.xml',
            'report/account_report.xml',
            'report/layout.xml'
             ],
    'installable': True,
    'application': True,
}

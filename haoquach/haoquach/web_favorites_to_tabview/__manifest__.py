# -*- coding: utf-8 -*-
{
    "name": "Favorites to TabView",
    "category": "web",
    "sequence": 14,
    "version": "12.0.1.0.1",
    'license': 'LGPL-3',
    "summary": "Configuration Favorites to TabView",
    "description": """
        Configuration Favorites to TabView.
    """,
    "author": "TGL team",
    "website": "https://trinhgialac.com",
    "depends": ["web"],
    "data": [
        "views/template_view.xml",
        "views/ir_filters_views.xml",
    ],
    "qweb": ["static/src/xml/*.xml"],
    "images": ["static/description/icon.png"],
    "application": False,
    "installable": True,
}

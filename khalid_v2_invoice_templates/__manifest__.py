# -*- coding: utf-8 -*-

{
    'name': 'Tholol Invoice Templates',
    'version': '13.0.0.0',
    'category': 'Tools',
    'author': 'Tholol',
    'depends': ['web', 'base', 'account','account_custom','base_vat'],
    'data': [

        "res_company.xml",
        "report/invoice_template.xml",

    ],
    'demo': [],
    'test': [],
    'assets': {
        'web.report_assets_common': [
            '/khalid_v2_invoice_templates/static/description/src/css/style.css',
        ],
    },
    'installable': True,
    'auto_install': False,
    "images": ['static/description/Banner.png'],
}

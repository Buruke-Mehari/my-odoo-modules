{
    'name': 'Dynamic Product Specifications',
    'summary': 'Add user-defined text, date, and selection fields to products',
    'version': '1.0',
    'category': 'Productivity',
    'depends': ['base','product','account'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template.xml',
    ],
    'installable': True,
    'application': False,
}
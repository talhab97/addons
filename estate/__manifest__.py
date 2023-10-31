{
    'name': "Real-Estate Management",
    'version': '1.0',
    'depends': ['base'],
    'author': "Talha Butt",
    'sequence': 0,
    'category': 'Category',
    'description': """
  This is a test module of Real-Estate Management!
  Written for the Odoo Quickstart Tutorial.
  """,

    # data files always loaded at installation

    'data': ['security/ir.model.access.csv',
             'views/estate_menu.xml',
             'views/estate_property_views.xml',
             'views/estate_pt_views.xml'],

    'installable': True,
    'auto_install': False,
    'application': True,

}

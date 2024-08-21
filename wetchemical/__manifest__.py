# -*- coding: utf-8 -*-
{
    'name': 'Wetchemical',
    'version': '13.0.1.1',
    'summary': 'Personalizacion para WetChemical',
    'description': """
        Cambios especificos para WetChemical.
        """,
    'category': '',
    'author': "Diego Gonzalez-Campo",
    'company': 'Proyectos Agiles, S.A.',
    'maintainer': 'Proyectos Agiles, S.A.',
    'website': "https://www.inteligos.gt",
    'depends': [
        'base', 'crm', 'stock', 'sale'
    ],
    'data': [
        'views/crm_lead_view.xml',
        'views/sale_order.xml'
    ],

}

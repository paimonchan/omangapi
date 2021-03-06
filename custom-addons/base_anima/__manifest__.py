# -*- coding: utf-8 -*-
{
    'name': "base_anima",
    'summary': """Base Ani & Manga System""",
    'description': """Base Ani & Manga System""",
    'author': "Paimon",
    'category': 'Manga',
    'version': '0.1',
    'depends': ['base'],
    'data': [
        # load access model
        'security/ir.model.access.csv',
        # load view model
        'views/anima_attribute.xml',
        'views/manga_chapter.xml',
        'views/anima_author.xml',
        'views/anima_tag.xml',
        'views/manga.xml',
        'views/menu.xml',
    ],
}

# -*- coding: utf-8 -*-

from odoo import models

class mangadex(models.AbstractModel):
    _inherit = 'request'
    _name = 'source.mangadex'
    _description = 'Mangadex'
    _base_url_config_key = 'source_mangadex'

    def pull_manga(self):
        def _main_title(title_dict):
            titles = [title_dict[key] for key in title_dict.keys()]
            return len(titles) > 0 and titles[0] or str()

        def _desctruct_title(title_dict, alt_title_list):
            titles = []
            for lang, title in title_dict.items():
                titles.append(dict(title=title, lang=lang))
            # source alt_title using list structure
            # the reason is alt_title can have multiple same lang
            for title_data in alt_title_list:
                for lang, title in title_data.items():
                    titles.append(dict(title=title, lang=lang))
            return titles

        def _main_desc(desc_dict):
            descriptions = [desc_dict[key] for key in desc_dict.keys()]
            return len(descriptions) > 0 and descriptions[0] or str()

        def _destruct_desc(desc_dict):
            descriptions = []
            for lang, desc in desc_dict.items():
                descriptions.append(dict(desc=desc, lang=lang))
            return descriptions

        results = self.GET('/manga')
        manga_model = self.env['manga']
        manga_ids = self.env['manga']
        for result in result:
            manga_ids = manga_model.create(dict(

            ))
        return result
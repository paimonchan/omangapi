# -*- coding: utf-8 -*-

from odoo import models

class mangadex(models.AbstractModel):
    _inherit = 'request'
    _name = 'source.mangadex'
    _description = 'Mangadex'
    _base_url_config_key = 'source_mangadex'

    def pull_manga(self, limit=1, offset=False):
        def _construct_endpoint():
            sysparam = self.env['ir.config_parameter'].sudo()
            next_offset = offset or sysparam.get_param(const.PARAMS_MANGADEX_LATEST_MANGA_OFFSET, 0)
            endpoint = '/manga?limit={}&offset={}'.format(limit, next_offset)
            # don't update sysparams when offset is custom
            if not offset:
                sysparam.set_param(const.PARAMS_MANGADEX_LATEST_MANGA_OFFSET, next_offset + 1)
            return endpoint

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

        def _destruct_tags(tag_list):
            tags = []
            for tag_dict in tag_list:
                attributes = tag_dict.get('attributes') or dict()
                is_genre = attributes.get('group') == 'genre'
                name_dict = attributes.get('name') or dict()
                # get tag name enlish only, ignore other
                name = name_dict.get('en')
                tags.append(dict(
                    is_genere=is_genre,
                    name=name,
                ))
            return tags

        # main function logic
        
        results = self.GET(_construct_endpoint())
        manga_model = self.env['manga']
        manga_ids = self.env['manga']
        for result in result:
            manga_ids = manga_model.create(dict(

            ))
        return result
# -*- coding: utf-8 -*-

from odoo import models
from ..helpers import const
from odoo.addons.base_anima.helpers import const as anima_const

class mangadex(models.AbstractModel):
    _inherit = 'request'
    _name = 'source.mangadex'
    _description = 'Mangadex'
    _base_url_config_key = 'source_mangadex'

    def pull_manga(self, limit=1, offset=False):
        def _get_latest_offset():
            sysparam = self.env['ir.config_parameter'].sudo()
            next_offset = offset or int(sysparam.get_param(const.PARAMS_MANGADEX_LATEST_MANGA_OFFSET, 0))
            # don't update sysparams when offset is custom
            if not offset:
                sysparam.set_param(const.PARAMS_MANGADEX_LATEST_MANGA_OFFSET, next_offset + 1)
            return next_offset

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

        def _destruct_content_rating(content_rating):
            if content_rating == 'safe':
                return anima_const.CONTENT_RATING_SAFE
            return anima_const.CONTENT_RATING_MATURE
        
        def _destruct_status(status):
            if status == 'completed':
                return anima_const.STATE_COMPLETED
            elif status == 'hiatus':
                return anima_const.STATE_HIATUS
            elif status == 'cancelled':
                return anima_const.STATE_CANCELLED
            return anima_const.STATE_ONGOING

        def _destruct_tags(tag_list, publication_demographic=False):
            tags = []
            for tag_dict in tag_list:
                attributes = tag_dict.get('attributes') or dict()
                is_genre = attributes.get('group') == 'genre'
                name_dict = attributes.get('name') or dict()
                # get tag name enlish only, ignore other
                name = name_dict.get('en')
                tags.append(dict(
                    is_genre=is_genre,
                    name=name,
                ))
            # publication demographic = shounen, shoujo, josei, seinen
            if publication_demographic:
                tags.append(dict(
                    is_genre=True,
                    name=publication_demographic,
                ))
            return tags
        
        def _get_or_create_tag_ids(destruct_tags):
            tag_ids = self.env['anima.tag']
            tag_model = self.env['anima.tag']
            for tag in tags:
                # find name tag case insensitive
                tag_id = tag_model.search(
                    [('name', '=ilike', tag['name'])], limit=1)
                if not tag_id:
                    tag_id = tag_model.create(dict(
                        name=tag['name'],
                        is_genre=tag['is_genre'],
                    ))
                tag_ids |= tag_id
            return tag_ids

        # main function logic
        
        offset = offset or _get_latest_offset()
        params = dict(limit=limit, offset=offset)
        results = self.GET('/manga', params)
        datas = results.get('data', [])
        manga_model = self.env['manga']
        manga_ids = self.env['manga']
        for result in datas:
            source_id = result.get('id', False)
            exist = self.env['manga'].search([('source_id', '=', source_id)])
            # validate if source_id already pulled
            if exist:
                continue

            attributes = result.get('attributes') or dict()
            content_rating_datas = attributes.get('contentRating', str())
            pd = attributes.get('publicationDemographic', False)
            desc_datas = attributes.get('description', dict())
            alt_title_datas = attributes.get('altTitle', [])
            title_datas = attributes.get('title', dict())
            tag_datas = attributes.get('tags', [])
            status = attributes.get('state')

            content_rating = _destruct_content_rating(content_rating_datas)
            alt_titles = _desctruct_title(title_datas, alt_title_datas)
            main_title = _main_title(title_datas)
            alt_desc = _destruct_desc(desc_datas)
            tags = _destruct_tags(tag_datas, pd)
            main_desc = _main_desc(desc_datas)
            state = _destruct_status(status)

            title_ids = [(0, 0, dict(
                lang=d['lang'], 
                name=d['title'],
                type=anima_const.ATTRIBUTE_TYPE_TITTLE
            )) for d in alt_titles]

            desc_ids = [(0, 0, dict(
                lang=d['lang'],
                name=d['desc'],
                type=anima_const.ATTRIBUTE_TYPE_DESCRIPTION
            )) for d in alt_desc]
            
            tag_ids = [(4, tag.id) for tag in _get_or_create_tag_ids(tags)]

            manga_ids |= manga_model.create(dict(
                source=anima_const.MANGA_SOURCE_MANAGEDEX,
                content_rating=content_rating,
                description_ids=desc_ids or False,
                title_ids=title_ids or False,
                tag_ids=tag_ids or False,
                description=main_desc,
                source_id=source_id,
                name=main_title,
                state=state,
            ))
        return results
# -*- coding: utf-8 -*-

from odoo import models
from ..helpers import const
from odoo.addons.base_common.helpers import log
from odoo.addons.base_anima.helpers import const as anima_const

import logging
logger = logging.getLogger(__name__)

class mangadex(models.AbstractModel):
    _inherit = 'request'
    _name = 'source.mangadex'
    _description = 'Mangadex'
    _base_url_config_key = 'source_mangadex'

    def pull_manga(self, limit=1, offset=False, no_update_sysparam=False):
        def _get_latest_offset():
            sysparam = self.env['ir.config_parameter'].sudo()
            next_offset = offset or int(sysparam.get_param(const.PARAMS_MANGADEX_LATEST_MANGA_OFFSET, 0))
            return next_offset
        
        def _set_latest_offset(count):
            sysparam = self.env['ir.config_parameter'].sudo()
            offset = int(sysparam.get_param(const.PARAMS_MANGADEX_LATEST_MANGA_OFFSET, 0))
            sysparam.set_param(const.PARAMS_MANGADEX_LATEST_MANGA_OFFSET, offset + count)

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
            for tag in destruct_tags:
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
        
        def _destruct_author_source_ids(relationships):
            source_ids = [rel['id'] for rel in relationships if rel['type'] == 'author']
            return source_ids or []

        def _connect_existing_author(manga, author_source_ids):
            authors = self.env['anima.author'].search(
                [('source_id', 'in', author_source_ids)])
            if not authors:
                return
            manga.write(dict(author_ids=[(4, id,) for id in authors.ids]))
        
        def _connect_existing_chapter(manga):
            chapters = self.env['manga.chapter'].search(
                [('manga_source_id', '=', manga.source_id)])
            if not chapters:
                return
            manga.write(dict(chapter_ids=[(4, id) for id in chapters.ids]))
        
        def _destruct_cover_art(relationships):
            covers = [rel['id'] for rel in relationships if rel['type'] == 'cover']
            return covers and covers[0] or []
        
        def _main_cron():
            next_offset = offset or _get_latest_offset()
            params = dict(limit=limit, offset=next_offset)
            results = self.GET('/manga', params)
            datas = results.get('data', [])
            manga_model = self.env['manga']
            manga_ids = self.env['manga']
            for result in datas:
                relationships = result.get('relationships') or dict()
                attributes = result.get('attributes') or dict()
                version = attributes.get('version') or 1
                source_id = result.get('id') or False
                exist = self.env['manga'].search([
                    ('source', '=', anima_const.MANGA_SOURCE_MANGADEX),
                    ('source_id', '=', source_id),
                    ('version', '=', version),
                ])
                # validate if source_id already pulled
                if exist:
                    continue

                content_rating_datas = attributes.get('contentRating', str())
                pd = attributes.get('publicationDemographic') or False
                desc_datas = attributes.get('description') or dict()
                alt_title_datas = attributes.get('altTitle') or []
                title_datas = attributes.get('title') or dict()
                tag_datas = attributes.get('tags') or dict()
                status = attributes.get('status') or str()

                content_rating = _destruct_content_rating(content_rating_datas)
                alt_titles = _desctruct_title(title_datas, alt_title_datas)
                cover = _destruct_cover_art(relationships)
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

                manga = manga_model.create(dict(
                    source=anima_const.MANGA_SOURCE_MANGADEX,
                    content_rating=content_rating,
                    description_ids=desc_ids or False,
                    title_ids=title_ids or False,
                    tag_ids=tag_ids or False,
                    description=main_desc,
                    cover_filename=cover,
                    source_id=source_id,
                    name=main_title,
                    version=version,
                    state=state,
                ))
                author_source_ids = _destruct_author_source_ids(relationships)
                _connect_existing_author(manga, author_source_ids)
                _connect_existing_chapter(manga)
                manga_ids |= manga

            if not no_update_sysparam:
                # update next offset
                _set_latest_offset(len(datas))

            return manga_ids
        
        # main function logic
        try:
            _main_cron()
        except Exception as ex:
            log.error(self, str(ex))
            raise
    
    def pull_author(self, limit=1, offset=False, no_update_sysparam=False):
        def _get_latest_offset():
            sysparam = self.env['ir.config_parameter'].sudo()
            next_offset = offset or int(sysparam.get_param(const.PARAMS_MANGADEX_LATEST_AUTHOR_OFFSET, 0))
            return next_offset
        
        def _set_latest_offset(count):
            sysparam = self.env['ir.config_parameter'].sudo()
            offset = int(sysparam.get_param(const.PARAMS_MANGADEX_LATEST_AUTHOR_OFFSET, 0))
            sysparam.set_param(const.PARAMS_MANGADEX_LATEST_AUTHOR_OFFSET, offset + count)
        
        def _destruct_manga_source_ids(relationships):
            source_ids = [rel['id'] for rel in relationships if rel['type'] == 'manga']
            return source_ids or []
        
        def _prepare_social_media(attributes):
            medias = [
                'twitter', 'pixiv', 'melonBook', 
                'fanBox', 'booth', 'nicoVideo',
                'skeb', 'fantia', 'tumblr',
                'youtube', 'website'
            ]
            social_medias = [
                (0, 0, dict(name=val, type=key)) for key, val in 
                attributes.items() if (key in medias and val)
            ]
            return social_medias
        
        def _connect_existing_manga(author, manga_source_ids):
            mangas = self.env['manga'].search(
                [('source_id', 'in', manga_source_ids),])
            if not mangas:
                return
            author.write(dict(manga_ids=[(4, id,) for id in mangas.ids]))

        def _main_cron():
            next_offset = offset or _get_latest_offset()
            params = dict(limit=limit, offset=next_offset)
            results = self.GET('/author', params)
            datas = results.get('data', [])

            author_model = self.env['anima.author']
            author_ids = self.env['anima.author']
            for result in datas:
                relationships = result.get('relationships') or dict()
                attributes = result.get('attributes') or dict()
                name = attributes.get('name') or str()
                source_id = result.get('id') or str()
                
                # check if already exist
                exist = author_model.search(
                    [('source_id', '=', source_id),], limit=1)
                if exist:
                    continue

                social_media_ids = _prepare_social_media(attributes) or False
                author = author_model.create(dict(
                    social_ids=social_media_ids,
                    source_id=source_id,
                    name=name,
                ))
                manga_source_ids = _destruct_manga_source_ids(relationships)
                _connect_existing_manga(author, manga_source_ids)
                author_ids |= author

            if not no_update_sysparam:
                # update next offset
                _set_latest_offset(len(datas))
        
        # main function logic
        try:
            _main_cron()
        except Exception as ex:
            log.error(self, str(ex))
            raise

    def pull_manga_chapter(self, limit=1, offset=False, no_update_sysparam=False):
        def _get_latest_offset():
            sysparam = self.env['ir.config_parameter'].sudo()
            next_offset = offset or int(sysparam.get_param(const.PARAMS_MANGADEX_LATEST_CHAPTER_OFFSET, 0))
            return next_offset
        
        def _set_latest_offset(count):
            sysparam = self.env['ir.config_parameter'].sudo()
            offset = int(sysparam.get_param(const.PARAMS_MANGADEX_LATEST_CHAPTER_OFFSET, 0))
            sysparam.set_param(const.PARAMS_MANGADEX_LATEST_CHAPTER_OFFSET, offset + count)
        
        def _destruct_manga_source_id(relationships):
            source_ids = [rel['id'] for rel in relationships if rel['type'] == 'manga']
            return source_ids and source_ids[0] or []

        def _prepare_manga_pages(low_images, high_images):
            pages = []
            for img in low_images:
                pages.append((0, 0, dict(
                    quality=anima_const.QUALITY_LOW,
                    filename=img,
                )))
            
            for img in high_images:
                pages.append((0, 0, dict(
                    quality=anima_const.QUALITY_HIGH,
                    filename=img,
                )))
            return pages or False
        
        def _get_manga_id(source_id):
            # get only one manga title
            manga_ids = self.env['manga'].search([
                ('source_id', '=', source_id)
            ], limit=1)
            return manga_ids
        
        def _main_cron():
            next_offset = offset or _get_latest_offset()
            params = dict(limit=limit, offset=next_offset)
            results = self.GET('/chapter', params)
            datas = results.get('data', [])

            chapter_model = self.env['manga.chapter']
            chapter_ids = self.env['manga.chapter']
            for result in datas:
                relationships = result.get('relationships') or dict()
                attributes = result.get('attributes') or dict()
                low_images = attributes.get('dataSaver') or []
                high_images = attributes.get('data') or []
                chapter = attributes.get('chapter') or 0
                volume = attributes.get('volume') or 0
                source_hash = attributes.get('hash') or str()
                source_id = result.get('id')

                # check if already exist
                exist = chapter_model.search(
                    [('source_id', '=', source_id),], limit=1)
                if exist:
                    continue

                page_ids = _prepare_manga_pages(low_images, high_images)
                manga_source_id = _destruct_manga_source_id(relationships)
                manga_id = _get_manga_id(manga_source_id)
                chapter = chapter_model.create(dict(
                    manga_source_id=manga_source_id,
                    manga_id=manga_id.id or False,
                    source_hash=source_hash,
                    source_id=source_id,
                    page_ids=page_ids,
                    chapter=chapter,
                    volume=volume,
                ))
                chapter_ids |= chapter

            if not no_update_sysparam:
                # update next offset
                _set_latest_offset(len(datas))
        
        # main function logic
        try:
            _main_cron()
        except Exception as ex:
            log.error(self, str(ex))
            raise
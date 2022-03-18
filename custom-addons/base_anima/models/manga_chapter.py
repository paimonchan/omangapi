# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MangaChapter(models.Model):
    _name = 'manga.chapter'
    _description = 'Manga Chapter'
    _rec_name = 'chapter'

    volume = fields.Char(default=0)
    chapter = fields.Char(required=True)
    manga_id = fields.Many2one('manga', 'Manga', ondelete='cascade')
    page_ids = fields.Many2one('manga.page', 'Manga Page')
    source_id = fields.Char(required=True)
    source_hash = fields.Char()
    manga_source_id = fields.Char(
        help='used to connect manga into chapter on new created manga entry')
    url = fields.Char()

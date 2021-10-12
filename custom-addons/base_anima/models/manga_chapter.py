# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MangaChapter(models.Model):
    _name = 'manga.chapter'
    _description = 'Manga Chapter'

    chapter = fields.Char(required=True)
    manga_id = fields.Many2one('manga', 'Manga', ondelete='cascade')
    page_ids = fields.Many2one('manga.page', 'Manga Page')
    source_id = fields.Char(required=True)
    url = fields.Char()

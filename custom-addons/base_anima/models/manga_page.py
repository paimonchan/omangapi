# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MangaPage(models.Model):
    _name = 'manga.page'
    _description = 'Manga Page'

    page = fields.Integer(required=True)
    chapter_id = fields.Many2one(
        'manga.chapter', 'Chapter', ondelete='cascade')
    url = fields.Char()    filename = fields.Char(required=True)
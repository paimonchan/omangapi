# -*- coding: utf-8 -*-

from odoo import models, fields, api
from ..helpers import const

class Manga(models.Model):
    _name = 'manga'
    _description = 'Manga'

    alt_name = fields.Char()
    description = fields.Text()
    name = fields.Char(required=True)
    source_id = fields.Char(required=True)
    source = fields.Selection(const.MANGA_SOURCE_SELECTION)
    chapter_ids = fields.One2many('manga.chapter', 'manga_id')
    chapter_count = fields.Integer(compute='_compute_chapter_count', store=True)
    tag_ids = fields.Many2many('anima.tag')
    tag_normalize = fields.Char(compute='_compute_tags')
    genre_normalize = fields.Char(compute='_compute_tags')
    title_ids = fields.One2many(
        'anima.attribute', 'manga_id', domain=[('type', '=', const.ATTRIBUTE_TYPE_TITTLE)])
    title_normalize = fields.Char(compute='_compute_titles')

    @api.depends('chapter_ids')
    def _compute_chapter_count(self):
        for record in self:
            record.chapter_count = len(record.chapter_ids or [])

    @api.depends('tag_ids')
    def _compute_tags(self):
        for record in self:
            tag_ids = record.tag_ids
            genre_ids = tag_ids.filtered(lambda t: t.genre)
            self.tags_normalize = ', '.join(tag_ids.mapped('name'))
            self.genres_normalize = ', '.join(genre_ids.mapped('name'))

    @api.depends('title_ids')
    def _compute_titles(self):
        for record in self:
            title_ids = record.title_ids
            self.title_normalize = ', '.join(title_ids.mapped('name'))
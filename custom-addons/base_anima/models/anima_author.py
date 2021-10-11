# -*- coding: utf-8 -*-

from odoo import models, fields
from ..helpers import const

class AnimaAuthor(models.Model):
    _name = 'anima.author'
    _description = 'Author'

    name = fields.Char(required=True)
    manga_ids = fields.Many2many(
        'manga', 'manga_author_rel', 'author_id', 'manga_id')
    social_ids = fields.One2many(
        'anima.social.media', 'author_id')
    source_id = fields.Char()
# -*- coding: utf-8 -*-

from odoo import models, fields
from ..helpers import const

class AnimaAttribute(models.Model):
    _name = 'anima.attribute'

    manga_id = fields.Many2one(
        'manga', ondelete='cascade')
    name = fields.Char(required=True)
    lang = fields.Char(
        help='Language Type, examples: en, zh, id')
    type = fields.Selection(
        const.ATTRIBUTES_TYPE_SELECTION, required=True)
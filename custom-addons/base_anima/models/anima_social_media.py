# -*- coding: utf-8 -*-

from odoo import models, fields
from ..helpers import const

class AnimaSocialMedia(models.Model):
    _name = 'anima.social.media'
    _description = 'Social Media'
    _rec_name = 'type'

    author_id = fields.Many2one('anima.author')
    type = fields.Selection(
        const.SOCIAL_MEDIAL_TYPE_SELECTION, required=True)
    name = fields.Char()
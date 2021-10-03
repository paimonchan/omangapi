# -*- coding: utf-8 -*-

from odoo import models, fields
from random import randint

class AnimaTag(models.Model):
    _name = 'anima.tag'

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char(required=True)
    is_genre = fields.Boolean(default=False)
    color = fields.Integer(default=_get_default_color)
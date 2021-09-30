# -*- coding: utf-8 -*-

from odoo import models, fields

class AnimaTag(models.Model):
    _name = 'anima.tag'

    name = fields.Char(required=True)
    is_genre = fields.Boolean(default=False)
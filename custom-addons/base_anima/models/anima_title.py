from odoo import models, fields

class AnimaTitle(models.Model):
    _name = 'anima.title'

    manga_id = fields.Many2one('manga')
    lang = fields.char()
from odoo import models, fields
from ..helpers import const

class AnimaAttribute(models.Model):
    _name = 'anima.attribute'

    manga_id = fields.Many2one('manga')
    name = fields.Char(required=True)
    lang = fields.char(
        help='Language Type, examples: en, zh, id')
    type = fields.Selection(
        const.ATTRIBUTES_TYPE_SELECTION, required=True)
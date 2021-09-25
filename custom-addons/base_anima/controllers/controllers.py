# -*- coding: utf-8 -*-
# from odoo import http


# class BaseManga(http.Controller):
#     @http.route('/base_manga/base_manga/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/base_manga/base_manga/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('base_manga.listing', {
#             'root': '/base_manga/base_manga',
#             'objects': http.request.env['base_manga.base_manga'].search([]),
#         })

#     @http.route('/base_manga/base_manga/objects/<model("base_manga.base_manga"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('base_manga.object', {
#             'object': obj
#         })

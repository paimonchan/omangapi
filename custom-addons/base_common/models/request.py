# -*- coding: utf-8 -*-

import json
import logging
import requests

from odoo import models
from werkzeug import urls
from odoo.tools import config

logger = logging.getLogger(__name__)

class Request(models.AbstractModel):
    _name = 'request'
    _base_url_config_key = ''

    def _construct_url(self, endpoint):
        base_url = config.get(self._base_url_config_key)
        return urls.url_join(base_url, endpoint)

    def POST(self, endpoint, data, header):
        default_headers = {
            'Content-Type': 'application/json', 
            'Accept': 'application/json', 
            'Catch-Control': 'no-cache'
        }
        header = {**default_headers, **header}
        url = self._construct_url(endpoint)
        try:
            response = requests.post(
                url, data=data, headers=header)
            return response.json()
        except requests.exceptions.Timeout:
            logger.error("request post timeout for url %s", url)
            raise
        except Exception:
            logger.error("request post bad request response")
            raise
    
    def GET(self, endpoint, params = dict(), header = dict()):
        default_headers = {
            'Content-Type': 'application/json', 
            'Accept': 'application/json', 
            'Catch-Control': 'no-cache'
        }
        header = {**default_headers, **header}
        url = self._construct_url(endpoint)
        try:
            response = requests.get(
                url, params=params, headers=header)
            return response.json()
        except requests.exceptions.Timeout:
            logger.error("request get timeout for url %s", url)
            raise
        except Exception:
            logger.error("request get bad request response")
            raise
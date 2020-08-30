# -*- coding: utf-8 -*-
"""Part of odoo. See LICENSE file for full copyright and licensing details."""

import functools
import logging
import urllib

from odoo import http
from odoo.addons.mobile_api.common import (
    extract_arguments,
    invalid_response,
    valid_response,
)
from odoo.http import request

_logger = logging.getLogger(__name__)

# _routes = ["/api/public/<model>", "/api/public/<model>/<id>", "/api/public/<model>/<id>/<action>"]

class APIController(http.Controller):
    """."""

    def __init__(self):
        self._model = "vidoo.mobile.api"

    @http.route('/api/public/<path:path>', type="http", auth="none", methods=["GET"], csrf=False)
    def mobile_api_only_get_data(self, model=None, id=None, **payload):
        ioc_name = http.request.httprequest.path
        record = request.env[self._model].sudo().search([("route", "=", ioc_name)], limit=1)
        if record:
            data = record.sudo().get_data()

            if data:
                return valid_response(data)
            else:
                return valid_response(data)
        return invalid_response(
            "invalid object model",
            "The model %s is not available in the registry." % ioc_name,
        )

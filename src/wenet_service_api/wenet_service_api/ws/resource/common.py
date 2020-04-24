from __future__ import absolute_import, annotations

import logging

from flask import request
from flask_restful import Resource, abort

logger = logging.getLogger("wenet_service_api.wenet_service_api.ws.resource.authenticated_resource")


class AuthenticatedResource(Resource):

    def __init__(self, authorized_api_key: str) -> None:
        super().__init__()
        self._authorized_api_key = authorized_api_key

    def _check_authentication(self):
        api_key = request.headers.get("apikey")

        if not api_key:
            logger.warning(f"Missing apikey header in request from [{request.remote_addr}], user agent: [{request.user_agent}]")
            abort(403, message="Missing apikey header")

        if api_key != self._authorized_api_key:
            logger.warning(f"Invalid apikey in request from [{request.remote_addr}], user agent: [{request.user_agent}]")
            abort(403, message="Invalid apikey")

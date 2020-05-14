from __future__ import absolute_import, annotations

import logging
from enum import Enum

from flask import request
from flask_restful import Resource, abort

from wenet_service_api.common.exception.exceptions import ResourceNotFound
from wenet_service_api.dao.dao_collector import DaoCollector

logger = logging.getLogger("api.api.ws.resource.authenticated_resource")


class WenetSources(Enum):

    APP = "app"
    COMPONENT = "component"


class AuthenticatedResource(Resource):

    def __init__(self, authorized_api_key: str, dao_collector: DaoCollector) -> None:
        super().__init__()
        self._authorized_api_key = authorized_api_key
        self._dao_collector = dao_collector

    def _check_authentication(self):
        wenet_source_str = request.headers.get("x-wenet-source")

        if not wenet_source_str:
            logger.warning(f"Missing x-wenet-source header in request from [{request.remote_addr}], user agent: [{request.user_agent}]")
            abort(401, message="Missing x-wenet-source header")

        try:
            wenet_source = WenetSources(wenet_source_str)
            logger.info(f"request from [{request.remote_addr}] from source [{wenet_source.value}], user agent: [{request.user_agent}]")
        except ValueError:
            logger.warning(
                f"Invalid x-wenet-source in request from [{request.remote_addr}], user agent: [{request.user_agent}]")
            abort(401, message="Invalid x-wenet-source")
            return

        if wenet_source == WenetSources.COMPONENT:
            api_key = request.headers.get("apikey")
            self._check_app_authentication(api_key)

        elif wenet_source == WenetSources.APP:

            app_id = request.headers.get("appId")
            app_token = request.headers.get("appToken")

            self._check_component_authentication(app_id, app_token)

        else:
            logger.error(f"Unable to authenticate with header [{wenet_source.value}]")
            abort(500)

    def _check_app_authentication(self, api_key) -> None:
        if not api_key:
            logger.warning(f"Missing apikey header in request from [{request.remote_addr}], user agent: [{request.user_agent}]")
            abort(401, message="Missing apikey header")

        if api_key != self._authorized_api_key:
            logger.warning(
                f"Invalid apikey in request from [{request.remote_addr}], user agent: [{request.user_agent}]")
            abort(401, message="Invalid apikey")

    def _check_component_authentication(self, app_id: str, app_token: str) -> None:

        if not app_id:
            logger.warning(f"Missing appId header in request from [{request.remote_addr}], user agent: [{request.user_agent}]")
            abort(401, message="Missing appId header")

        if not app_token:
            logger.warning(f"Missing appToken header in request from [{request.remote_addr}], user agent: [{request.user_agent}]")
            abort(401, message="Missing appToken header")

        try:
            app = self._dao_collector.app_dao.get(app_id)
        except ResourceNotFound:
            logger.warning(f"Unable to find an app with id [{app_id}] in request from [{request.remote_addr}], user agent: [{request.user_agent}]")
            abort(401, message="Not authorized")
            return
        except Exception as e:
            logger.exception(f"Unable to find the application with id [{app_id}]", exc_info=e)
            abort(500)
            return

        if app.app_token != app_token:
            logger.warning(f"Invalid token form app [{app_id}] in request from [{request.remote_addr}], user agent: [{request.user_agent}]")
            abort(401, message="Not authorized")

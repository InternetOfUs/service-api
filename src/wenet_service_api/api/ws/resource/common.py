from __future__ import absolute_import, annotations

import logging
from enum import Enum
from typing import List, Optional

from flask import request
from flask_restful import Resource, abort

from wenet.common.model.app.app_dto import AppStatus, App
from wenet.common.model.scope import Scope
from wenet_service_api.common.exception.exceptions import ResourceNotFound
from wenet_service_api.connector.collector import ServiceConnectorCollector

logger = logging.getLogger("api.api.ws.resource.authenticated_resource")


class WenetSource(Enum):

    COMPONENT = "component"
    OAUTH2_AUTHORIZATION_CODE = "oauth2_authorization_code"


class AuthenticationResult:

    def __init__(self, source: WenetSource):
        self.source = source

    def to_repr(self) -> dict:
        return {
            "source": self.source
        }

    def __eq__(self, o) -> bool:
        if not isinstance(o, AuthenticationResult):
            return False
        return o.source == self.source

    def __repr__(self) -> str:
        return str(self.to_repr())

    def __str__(self) -> str:
        return self.__repr__()


class ComponentAuthentication(AuthenticationResult):

    def __init__(self):
        super().__init__(WenetSource.COMPONENT)


class AppAuthentication(AuthenticationResult):

    def __init__(self, app_id: str):
        super().__init__(WenetSource.APP)
        self.app_id = app_id

    def to_repr(self) -> dict:
        base_repr = super().to_repr()
        base_repr.update({
            "appId": self.app_id
        })
        return base_repr

    def __eq__(self, o) -> bool:
        if not isinstance(o, AppAuthentication):
            return False
        return super().__eq__(o) and o.app_id == self.app_id


class Oauth2Result(AuthenticationResult):

    def __init__(self, wenet_user_id: Optional[str], scopes: Optional[List[Scope]], app: Optional[App]):
        super().__init__(WenetSource.OAUTH2_AUTHORIZATION_CODE)
        self.wenet_user_id = wenet_user_id
        self.scopes = scopes
        self.app = app

    def to_repr(self) -> dict:
        base_repr = super().to_repr()
        base_repr.update({
            "wenetUserId": self.wenet_user_id,
            "scopes": list(x.value for x in self.scopes) if self.scopes is not None else None,
            "app": self.app.to_repr() if self.app is not None else None
        })
        return base_repr

    def __eq__(self, o) -> bool:
        if not isinstance(o, Oauth2Result):
            return False
        return super().__eq__(o) and o.wenet_user_id == self.wenet_user_id and o.scopes == self.scopes and o.app == self.app

    def has_scope(self, scope: Scope) -> bool:
        return scope in self.scopes


class AuthenticatedResource(Resource):

    def __init__(self, authorized_api_key: str, connector_collector: ServiceConnectorCollector) -> None:
        super().__init__()
        self._authorized_api_key = authorized_api_key
        self._service_connector_collector = connector_collector

    @staticmethod
    def _get_user_id(authentication_result: AuthenticationResult) -> str:

        if isinstance(authentication_result, Oauth2Result):
            return authentication_result.wenet_user_id
        else:
            profile_id = request.headers.get("X-Wenet-Userid")
            if profile_id is None or profile_id == "":
                abort(400, message="missing X-Wenet-Userid header")
                return
            else:
                return profile_id

    def _check_authentication(self, supported_sources: List[WenetSource]) -> AuthenticationResult:
        """
        Check the authentication and in case of success it return an AuthenticationResult with the login information,
        in case of failure it abort the request with the appropriate error code
        @param supported_sources: A list of supported authentication method for the endpoint
        @return:
        """
        wenet_source_str = request.headers.get("x-wenet-source")

        logger.debug("REQUEST HEADERS")
        for header in request.headers:
            logger.debug(f"\t{header}")

        if not wenet_source_str:
            logger.warning(f"Missing x-wenet-source header in request from [{request.remote_addr}], user agent: [{request.user_agent}]")
            abort(401, message="Missing x-wenet-source header")

        try:
            wenet_source = WenetSource(wenet_source_str)
            logger.info(f"request from [{request.remote_addr}] from source [{wenet_source.value}], user agent: [{request.user_agent}]")
        except ValueError:
            logger.warning(
                f"Invalid x-wenet-source in request from [{request.remote_addr}], user agent: [{request.user_agent}]")
            abort(401, message="Invalid x-wenet-source")
            return

        if wenet_source not in supported_sources:
            abort(401, message=f"Authentication of type {wenet_source.value} not supported for this route")
            return

        if wenet_source == WenetSource.COMPONENT:
            api_key = request.headers.get("apikey")
            self._check_apikey_authentication(api_key)
            return ComponentAuthentication()

        elif wenet_source == WenetSource.OAUTH2_AUTHORIZATION_CODE:

            api_key = request.headers.get("apikey")
            self._check_apikey_authentication(api_key)

            authenticated_user_id = request.headers.get("X-Authenticated-Userid")
            scopes = request.headers.get("X-Authenticated-Scope")
            consumer_id = request.headers.get("X-Consumer-Username")

            return self._check_oauth2_code_authentication(authenticated_user_id, scopes, consumer_id)

        else:
            logger.error(f"Unable to authenticate with header [{wenet_source.value}]")
            abort(500)

    def _check_apikey_authentication(self, api_key) -> None:
        if not api_key:
            logger.warning(f"Missing apikey header in request from [{request.remote_addr}], user agent: [{request.user_agent}]")
            abort(401, message="Missing apikey header")

        if api_key != self._authorized_api_key:
            logger.warning(
                f"Invalid apikey in request from [{request.remote_addr}], user agent: [{request.user_agent}]")
            abort(401, message="Invalid apikey")

    def _check_oauth2_code_authentication(self, authenticated_user_id: Optional[str], scopes_str: Optional[str], consumer_id: Optional[str]) -> Oauth2Result:
        if authenticated_user_id is None or authenticated_user_id == "":
            abort(401, message="Missing userid or scopes")

        if scopes_str is None or scopes_str == "":
            abort(401, message="Missing userid or scopes")

        if consumer_id is None or consumer_id == "":
            abort(401, message="Missing consumer id")

        try:
            scopes = list(Scope(x) for x in scopes_str.split(" "))
        except ValueError:
            abort(403, message="Invalid scopes")

        app_id = consumer_id.replace("app_", "")

        try:
            app = self._service_connector_collector.hub_connector.get_app(app_id)
        except ResourceNotFound:
            logger.info(f"Invalid app [{app_id}]")
            abort(403, message="Invalid app")
            return
        except Exception as e:
            logger.exception(f"Unable to find the app with id [{app_id}]", exc_info=e)
            abort(403, message="Invalid app")
            return

        if app.status == AppStatus.ACTIVE:
            return Oauth2Result(authenticated_user_id, scopes, app)
        else:

            developers = self._service_connector_collector.hub_connector.get_app_developers(app_id)
            logger.debug(f"{len(developers)} for app")
            for dev in developers:
                logger.debug(f"dev: {dev}")
                if str(dev) == authenticated_user_id:
                    logger.debug(f"User [{authenticated_user_id}] is a developer of the app [{app_id}]")
                    return Oauth2Result(authenticated_user_id, scopes, app)

            abort(403, message="The application is in development mode, only the developer can access it")
            return





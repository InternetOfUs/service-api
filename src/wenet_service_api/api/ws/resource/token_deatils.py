from __future__ import absolute_import, annotations

import logging

from flask_restful import abort
from wenet.interface.exceptions import NotFound, BadRequest

from wenet.model.user.token import TokenDetails
from wenet_service_api.api.ws.resource.common import AuthenticatedResource, WenetSource, Oauth2Result
from wenet_service_api.connector.collector import ServiceConnectorCollector

logger = logging.getLogger("api.api.ws.resource.token_details")


class TokenDetailsInterfaceBuilder:

    @staticmethod
    def routes(service_connector_collector: ServiceConnectorCollector, authorized_apikey: str):
        return [
            (TokenDetailsInterface, "", (service_connector_collector, authorized_apikey))
        ]


class TokenDetailsInterface(AuthenticatedResource):

    def __init__(self, service_connector_collector: ServiceConnectorCollector, authorized_apikey: str) -> None:
        super().__init__(authorized_apikey, service_connector_collector)

    def get(self):
        authentication_result = self._check_authentication([WenetSource.OAUTH2_AUTHORIZATION_CODE])

        if not isinstance(authentication_result, Oauth2Result):
            abort(400)
            return

        profile_id = self._get_user_id(authentication_result)

        try:
            profile = self._service_connector_collector.profile_manager_collector.get_user_profile(profile_id)
            logger.info(f"Retrieved profile [{profile_id}] from profile manager connector")
        except (NotFound, BadRequest) as e:
            logger.info(f"Unable to retrieve the token details, server replay with [{e.http_status_code}] [{e.server_response}]")
            return self.build_api_exception_response(e)
        except Exception as e:
            logger.exception("Unable to retrieve the profile", exc_info=e)
            abort(500)
            return

        scopes = list(scope.value for scope in authentication_result.scopes)
        token_details = TokenDetails(profile.profile_id, authentication_result.app.app_id, scopes)
        return token_details.to_repr(), 200

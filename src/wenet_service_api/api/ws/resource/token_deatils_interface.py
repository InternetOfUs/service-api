from __future__ import absolute_import, annotations

import logging

from flask_restful import abort

from wenet.common.model.user.token_details import TokenDetails
from wenet_service_api.api.ws.resource.common import AuthenticatedResource, WenetSource, Oauth2Result
from wenet_service_api.api.ws.resource.utils.user_profile import filter_user_profile
from wenet_service_api.common.exception.exceptions import ResourceNotFound, NotAuthorized
from wenet_service_api.connector.collector import ServiceConnectorCollector
from wenet_service_api.dao.dao_collector import DaoCollector

logger = logging.getLogger("api.api.ws.resource.token_details")


class TokenDetailsInterfaceBuilder:

    @staticmethod
    def routes(service_connector_collector: ServiceConnectorCollector, authorized_apikey: str,
               dao_collector: DaoCollector):
        return [
            (TokenDetailsInterface, "", (service_connector_collector, authorized_apikey, dao_collector))
        ]


class TokenDetailsInterface(AuthenticatedResource):

    def __init__(self, service_connector_collector: ServiceConnectorCollector, authorized_apikey: str,
                 dao_collector: DaoCollector) -> None:
        super().__init__(authorized_apikey, dao_collector)
        self._service_connector_collector = service_connector_collector

    def get(self):
        authentication_result = self._check_authentication([WenetSource.OAUTH2_AUTHORIZATION_CODE])

        if not isinstance(authentication_result, Oauth2Result):
            abort(400)
            return

        profile_id = self._get_user_id(authentication_result)

        try:
            temp = self._service_connector_collector.profile_manager_collector.get_profile(profile_id)
            profile = filter_user_profile(temp, authentication_result)
            logger.info(f"Retrieved profile [{profile_id}] from profile manager connector")
        except ResourceNotFound as e:
            logger.exception("Unable to retrieve the profile", exc_info=e)
            abort(404, message="Resource not found")
            return
        except NotAuthorized as e:
            logger.exception(f"Unauthorized to retrieve the profile [{profile_id}]", exc_info=e)
            abort(403)
            return
        except Exception as e:
            logger.exception("Unable to retrieve the profile", exc_info=e)
            abort(500)
            return

        scopes = list(scope.value for scope in authentication_result.scopes)
        token_details = TokenDetails(profile.profile_id, authentication_result.app.app_id, scopes)
        return token_details.to_repr(), 200

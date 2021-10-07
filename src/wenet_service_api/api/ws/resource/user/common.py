from __future__ import absolute_import, annotations

import logging

from wenet_service_api.common.exception.exceptions import ResourceNotFound
from wenet_service_api.connector.collector import ServiceConnectorCollector
from wenet_service_api.api.ws.resource.common import AuthenticatedResource, AuthenticationResult, Oauth2Result, ComponentAuthentication

logger = logging.getLogger("api.api.ws.resource.user.core_profile")


class CommonWeNetUserInterface(AuthenticatedResource):

    def __init__(self, service_connector_collector: ServiceConnectorCollector, authorized_apikey: str) -> None:
        super().__init__(authorized_apikey, service_connector_collector)

    def _can_view_profile(self, authentication_result: AuthenticationResult, profile_id: str) -> bool:
        if isinstance(authentication_result, ComponentAuthentication):
            return True
        elif isinstance(authentication_result, Oauth2Result):
            try:
                user_ids = self._service_connector_collector.hub_connector.get_user_ids_for_app(app_id=authentication_result.app.app_id)
                return profile_id in user_ids
            except ResourceNotFound:
                return False
        else:
            return False

    @staticmethod
    def _is_owner(authentication_result: Oauth2Result, profile_id: str) -> bool:
        if not isinstance(authentication_result, Oauth2Result):
            raise Exception("is_owner method only accepts Oauth2Results")

        return authentication_result.wenet_user_id == profile_id

    @staticmethod
    def _can_edit_profile(authentication_result, profile_id: str) -> bool:
        if isinstance(authentication_result, ComponentAuthentication):
            return True
        elif isinstance(authentication_result, Oauth2Result):
            return CommonWeNetUserInterface._is_owner(authentication_result, profile_id)
        else:
            return False

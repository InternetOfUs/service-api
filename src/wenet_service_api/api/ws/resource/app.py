from __future__ import absolute_import, annotations

from flask_restful import abort

import logging

from wenet.interface.exceptions import AuthenticationException, NotFound
from wenet.model.app import AppDTO
from wenet_service_api.connector.collector import ServiceConnectorCollector
from wenet_service_api.api.ws.resource.common import AuthenticatedResource, WenetSource

logger = logging.getLogger("api.api.ws.resource.app")


class AppResourceInterfaceBuilder:

    @staticmethod
    def routes(service_connector_collector: ServiceConnectorCollector, authorized_apikey: str):
        return [
            (AppResourceInterface, "/<string:app_id>", (service_connector_collector, authorized_apikey)),
            (ListAppUserInterface, "/<string:app_id>/users", (service_connector_collector, authorized_apikey))
        ]


class AppResourceInterface(AuthenticatedResource):

    def __init__(self, service_connector_collector: ServiceConnectorCollector, authorized_apikey: str) -> None:
        super().__init__(authorized_apikey, service_connector_collector)

    def get(self, app_id: str):

        self._check_authentication([WenetSource.COMPONENT])

        try:
            app = self._service_connector_collector.hub_connector.get_app_details(app_id=app_id)
        except AuthenticationException as e:
            logger.exception(f"Unauthorized to retrieve the resource with id [{app_id}]", exc_info=e)
            abort(403)
            return
        except NotFound:
            logger.info(f"Resource with id [{app_id}] not found")
            abort(404, message=f"Resource with id [{app_id}] not found")
            return
        except Exception as e:
            logger.exception(f"Unable to retrieve the resource with id [{app_id}]", exc_info=e)
            abort(500, message=f"Unable to retrieve the resource with id [{app_id}]")
            return

        app_dto = AppDTO.from_app(app)
        logger.info(f"Retrieved app [{app_dto}]")
        return app_dto.to_repr(), 200


class ListAppUserInterface(AuthenticatedResource):

    def __init__(self, service_connector_collector: ServiceConnectorCollector, authorized_apikey: str) -> None:
        super().__init__(authorized_apikey, service_connector_collector)

    def get(self, app_id: str):

        self._check_authentication([WenetSource.COMPONENT])

        try:
            app = self._service_connector_collector.hub_connector.get_app_details(app_id)
            users = self._service_connector_collector.hub_connector.get_user_ids_for_app(app_id)
        except AuthenticationException as e:
            logger.exception(f"Unauthorized to retrieve the resource with id [{app_id}]", exc_info=e)
            abort(403)
            return
        except NotFound:
            abort(404, message="Application not found")
            return
        except Exception as e:
            logger.exception(f"Unable to retrieve the list of account for app {app_id}", exc_info=e)
            abort(500, message=f"Unable to retrieve the list of account for app {app_id}")
            return

        return users, 200

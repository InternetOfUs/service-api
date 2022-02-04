from __future__ import absolute_import, annotations

from flask_restful import abort

import logging

from wenet.interface.exceptions import NotFound, BadRequest
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
        except (NotFound, BadRequest) as e:
            logger.info(f"Unable to retrieve the application with id [{app_id}], server replay with [{e.http_status_code}] [{e.server_response}]")
            return self.build_api_exception_response(e)
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
            self._service_connector_collector.hub_connector.get_app_details(app_id)  # check if the application exist
            users = self._service_connector_collector.hub_connector.get_user_ids_for_app(app_id)
        except (NotFound, BadRequest) as e:
            logger.info(f"Unable to retrieve the list of user of the application with id [{app_id}], server replay with [{e.http_status_code}] [{e.server_response}]")
            return self.build_api_exception_response(e)
        except Exception as e:
            logger.exception(f"Unable to retrieve the list of account for app {app_id}", exc_info=e)
            abort(500, message=f"Unable to retrieve the list of account for app {app_id}")
            return

        return users, 200

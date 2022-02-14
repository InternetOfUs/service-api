from __future__ import absolute_import, annotations

import logging

from flask import request
from flask_restful import abort
from wenet.interface.exceptions import NotFound, BadRequest

from wenet_service_api.api.ws.resource.common import AuthenticatedResource, WenetSource
from wenet_service_api.connector.collector import ServiceConnectorCollector

logger = logging.getLogger("api.api.ws.resource.task_list")


class TaskListResourceInterfaceBuilder:

    @staticmethod
    def routes(service_connector_collector: ServiceConnectorCollector, authorized_apikey: str):
        return [
            (TaskListResourceInterface, "", (service_connector_collector, authorized_apikey))
        ]


class TaskListResourceInterface(AuthenticatedResource):

    def __init__(self, service_connector_collector: ServiceConnectorCollector, authorized_apikey: str) -> None:
        super().__init__(authorized_apikey, service_connector_collector)

    def get(self):
        self._check_authentication([WenetSource.COMPONENT, WenetSource.OAUTH2_AUTHORIZATION_CODE])

        app_id = request.args.get('appId', None)
        requester_id = request.args.get('requesterId', None)
        task_type_id = request.args.get('taskTypeId', None)
        goal_name = request.args.get('goalName', None)
        goal_description = request.args.get('goalDescription', None)
        creation_from = request.args.get('creationFrom', None)
        creation_to = request.args.get('creationTo', None)
        update_from = request.args.get('updateFrom', None)
        update_to = request.args.get('updateTo', None)
        has_close_ts = request.args.get('hasCloseTs', None)
        close_from = request.args.get('closeFrom', None)
        close_to = request.args.get('closeTo', None)
        order = request.args.get('order', None)
        offset = request.args.get('offset', None)
        limit = request.args.get('limit', None)

        try:
            task_page = self._service_connector_collector.task_manager_connector.get_task_page(
                app_id=app_id,
                requester_id=requester_id,
                task_type_id=task_type_id,
                goal_name=goal_name,
                goal_description=goal_description,
                creation_from=creation_from,
                creation_to=creation_to,
                update_from=update_from,
                update_to=update_to,
                has_close_ts=has_close_ts,
                closed_from=close_from,
                closed_to=close_to,
                order=order,
                offset=offset,
                limit=limit
            )
        except (NotFound, BadRequest) as e:
            logger.info(f"Unable to retrieve the task list, server replay with [{e.http_status_code} [{e.server_response}]")
            return self.build_api_exception_response(e)
        except Exception as e:
            logger.exception("Unable to retrieve the task", exc_info=e)
            abort(500)
            return

        return task_page.to_repr(), 200

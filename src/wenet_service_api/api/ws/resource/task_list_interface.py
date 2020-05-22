from __future__ import absolute_import, annotations

import logging

from flask import request
from flask_restful import abort

from wenet_service_api.api.ws.resource.common import AuthenticatedResource
from wenet_service_api.common.exception.exceptions import NotAuthorized
from wenet_service_api.connector.collector import ServiceConnectorCollector
from wenet_service_api.dao.dao_collector import DaoCollector

logger = logging.getLogger("api.api.ws.resource.task_list")


class TaskListResourceInterfaceBuilder:

    @staticmethod
    def routes(service_connector_collector: ServiceConnectorCollector, authorized_apikey: str, dao_collector: DaoCollector):
        return [
            (TaskListResourceInterface, "", (service_connector_collector, authorized_apikey, dao_collector))
        ]


class TaskListResourceInterface(AuthenticatedResource):

    def __init__(self, service_connector_collector: ServiceConnectorCollector, authorized_apikey: str, dao_collector: DaoCollector) -> None:
        super().__init__(authorized_apikey, dao_collector)
        self._service_connector_collector = service_connector_collector

    def get(self):
        self._check_authentication()

        app_id = request.args.get('appId', None)
        requester_id = request.args.get('requesterId', None)
        task_type_id = request.args.get('taskTypeId', None)
        goal_name = request.args.get('goalName', None)
        goal_description = request.args.get('goalDescription', None)
        start_from = request.args.get('startFrom', None)
        start_to = request.args.get('startTo', None)
        end_from = request.args.get('endFrom', None)
        end_to = request.args.get('endTo', None)
        deadline_from = request.args.get('deadlineFrom', None)
        deadline_to = request.args.get('deadlineTo', None)
        offset = request.args.get('offset', None)
        limit = request.args.get('limit', None)

        try:
            task_page = self._service_connector_collector.task_manager_connector.get_tasks(
                app_id=app_id,
                requester_id=requester_id,
                task_type_id=task_type_id,
                goal_name=goal_name,
                goal_description=goal_description,
                start_from=start_from,
                start_to=start_to,
                end_from=end_from,
                end_to=end_to,
                deadline_from=deadline_from,
                deadline_to=deadline_to,
                offset=offset,
                limit=limit
            )
        except NotAuthorized as e:
            logger.exception(f"Unauthorized to retrieve the task list", exc_info=e)
            abort(403)
            return
        except Exception as e:
            logger.exception("Unable to retrieve the task", exc_info=e)
            abort(500)
            return

        return task_page.to_repr(), 200

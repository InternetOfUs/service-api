from __future__ import absolute_import, annotations

import logging
from typing import Optional

from flask import request
from flask_restful import abort
from wenet.interface.exceptions import NotFound, BadRequest

from wenet.model.task.task import Task
from wenet_service_api.connector.collector import ServiceConnectorCollector
from wenet_service_api.api.ws.resource.common import AuthenticatedResource, WenetSource

logger = logging.getLogger("api.api.ws.resource.task")


class TaskResourceInterfaceBuilder:

    @staticmethod
    def routes(service_connector_collector: ServiceConnectorCollector, authorized_apikey: str):
        return [
            (TaskResourceInterface, "/<string:task_id>", (service_connector_collector, authorized_apikey)),
            (TaskResourcePostInterface, "", (service_connector_collector, authorized_apikey))
        ]


class TaskResourceInterface(AuthenticatedResource):

    def __init__(self, service_connector_collector: ServiceConnectorCollector, authorized_apikey: str) -> None:
        super().__init__(authorized_apikey, service_connector_collector)

    def get(self, task_id: str):

        self._check_authentication([WenetSource.COMPONENT, WenetSource.OAUTH2_AUTHORIZATION_CODE])

        try:
            task = self._service_connector_collector.task_manager_connector.get_task(task_id)
            logger.info(f"Retrieved task [{task_id}] from task manager connector")
        except (NotFound, BadRequest) as e:
            logger.info(f"Unable to retrieve the task, server replay with [{e.http_status_code}] [{e.server_response}]")
            return self.build_api_exception_response(e)
        except Exception as e:
            message = f"Unable to retrieve the task with id [{task_id}]"
            logger.exception(message, exc_info=e)
            abort(500, message=message)
            return

        return task.to_repr(), 200

    def put(self, task_id: str):
        self._check_authentication([WenetSource.COMPONENT, WenetSource.OAUTH2_AUTHORIZATION_CODE])

        # Will raise a BadRequest if an invalid json is provided with the ContentType application/json. None with a different ContentType
        posted_data: Optional[dict] = request.get_json()

        if posted_data is None:
            abort(400, message="The body should be a json object")
            return

        # remove id from body, the id in the path parameter is used
        posted_data["taskId"] = task_id
        try:
            task = Task.from_repr(posted_data)
        except (ValueError, TypeError):
            logger.info(f"Unable to build a Task from [{posted_data}]")
            abort(400, message="The body is not a valid task")
            return
        except KeyError as k:
            logger.info(f"Unable to build a Task from [{posted_data}]")
            abort(400, message=f"The field [{k}] is missing")
            return

        try:
            self._service_connector_collector.task_manager_connector.update_task(task)
        except (NotFound, BadRequest) as e:
            logger.info(f"Unable to refresh the task with id [{task_id}] server replay with [{e.http_status_code}] [{e.server_response}]")
            return self.build_api_exception_response(e)
        except Exception as e:
            logger.exception(f"Unable to update the task with id [{task_id}]", exc_info=e)
            abort(500, message=f"Unable to update the task with id [{task_id}]")
            return

        logger.info(f"Updated task [{task_id}]")
        return task.to_repr(), 200


class TaskResourcePostInterface(AuthenticatedResource):

    def __init__(self, service_connector_collector: ServiceConnectorCollector, authorized_apikey: str) -> None:
        super().__init__(authorized_apikey, service_connector_collector)

    def post(self):
        self._check_authentication([WenetSource.COMPONENT, WenetSource.OAUTH2_AUTHORIZATION_CODE])

        # Will raise a BadRequest if an invalid json is provided with the ContentType application/json. None with a different ContentType
        posted_data: Optional[dict] = request.get_json()

        if posted_data is None:
            abort(400, message="The body should be a json object")
            return

        try:
            task = Task.from_repr(posted_data)
        except (ValueError, TypeError) as v:
            logger.exception("Unable to build a Task from [%s]" % posted_data, exc_info=v)
            abort(400, message="Some fields contains invalid parameters")
            return
        except KeyError as k:
            logger.exception("Unable to build a Task from [%s]" % posted_data, exc_info=k)
            abort(400, message="The field [%s] is missing" % k)
            return

        try:
            created_task = self._service_connector_collector.task_manager_connector.create_task(task)
        except BadRequest as e:
            logger.info(f"Bad request response during task creation for task [{task}], server replay with [{e.http_status_code}] [{e.server_response}]")
            return self.build_api_exception_response(e)
        except Exception as e:
            logger.exception(f"Unable to create the task [{task}]", exc_info=e)
            abort(500, message="Unable to create the task")
            return

        logger.info(f"Created task [{created_task.task_id}]")
        return created_task.to_repr(), 201

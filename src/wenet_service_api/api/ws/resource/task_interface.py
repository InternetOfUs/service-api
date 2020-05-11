from __future__ import absolute_import, annotations

import logging
import uuid

from flask import request
from flask_restful import abort

from wenet.common.model.task.task import Task
from wenet_service_api.common.exception.exceptions import ResourceNotFound, NotAuthorized, BadRequestException
from wenet_service_api.connector.collector import ServiceConnectorCollector
from wenet_service_api.api.ws.resource.common import AuthenticatedResource

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
        super().__init__(authorized_apikey)
        self.service_connector_collector = service_connector_collector

    def get(self, task_id: str):

        self._check_authentication()

        try:
            task = self.service_connector_collector.task_manager_connector.get_task(task_id)
            logger.info(f"Retrieved task [{task_id}] from task manager connector")
        except ResourceNotFound as e:
            logger.exception("Unable to retrieve the task", exc_info=e)
            abort(404, message="Resource not found")
            return
        except NotAuthorized as e:
            logger.exception(f"Unauthorized to retrieve the task [{task_id}]", exc_info=e)
            abort(403)
            return
        except Exception as e:
            logger.exception("Unable to retrieve the task", exc_info=e)
            abort(500)
            return

        return task.to_repr(), 200

    def put(self, task_id: str):
        self._check_authentication()

        try:
            posted_data: dict = request.get_json()
        except Exception as e:
            logger.exception("Invalid message body", exc_info=e)
            abort(400, message="Invalid JSON - Unable to parse message body")
            return

        # remove id from body, the id in the path parameter is used
        posted_data["taskId"] = task_id
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
            updated_task = self.service_connector_collector.task_manager_connector.updated_task(task)
        except NotAuthorized as e:
            logger.exception(f"Unauthorized to update the task [{task_id}]", exc_info=e)
            abort(403)
            return
        except BadRequestException as e:
            logger.exception(f"Bad request exception during update for task [{task_id}] [{task}]", exc_info=e)
            abort(400, message=str(e))
            return
        except ResourceNotFound:
            logger.warning(f"Resource [{task_id}] not found")
            abort(404, message=f"Resource [{task_id}] not found")
            return
        except Exception as e:
            logger.exception("Unable to update the task", exc_info=e)
            abort(500)
            return

        logger.info(f"Updated task [{updated_task}]")
        return updated_task.to_repr(), 200


class TaskResourcePostInterface(AuthenticatedResource):

    def __init__(self, service_connector_collector: ServiceConnectorCollector, authorized_apikey: str) -> None:
        super().__init__(authorized_apikey)
        self._service_connector_collector = service_connector_collector

    def post(self):
        self._check_authentication()

        try:
            posted_data: dict = request.get_json()
        except Exception as e:
            logger.exception("Invalid message body", exc_info=e)
            abort(400, message="Invalid JSON - Unable to parse message body")
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
        except NotAuthorized as e:
            logger.exception(f"Not authorized to create the task [{task}]", exc_info=e)
            abort(403, message="Not authorized")
            return
        except BadRequestException as e:
            logger.exception(f"Bad request exception during creation of task [{task}]", exc_info=e)
            abort(400, message=str(e))
            return
        except Exception as e:
            logger.exception(f"Unable to create the task [{task}]", exc_info=e)
            abort(500, message="Unable to create the task")
            return

        logger.info(f"Created task [{task}]")
        return created_task.to_repr(), 201

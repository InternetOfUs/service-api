from __future__ import absolute_import, annotations

import logging
import uuid
from datetime import datetime

from flask import request
from flask_restful import Resource, abort

from wenet.model.norm import Norm, NormOperator
from wenet.model.task import Task, TaskState

logger = logging.getLogger("wenet.wenet_service_api.ws.resource.task")


class TaskResourceInterfaceBuilder:

    @staticmethod
    def routes():
        return [
            (TaskResourceInterface, "/<string:task_id>", ())
        ]


class TaskResourceInterface(Resource):

    def __init__(self) -> None:
        super().__init__()

    def get(self, task_id: str):
        task = Task(
            task_id=task_id,
            creation_ts=datetime(2020, 1, 21).timestamp(),
            state=TaskState.OPEN,
            requester_user_id=str(uuid.uuid4()),
            start_ts=datetime(2020, 1, 21).timestamp(),
            end_ts=None,
            deadline_ts=datetime.now().timestamp(),
            norms=[
                Norm(
                    norm_id=str(uuid.uuid4()),
                    attribute="has_car",
                    operator=NormOperator.EQUALS,
                    comparison=True,
                    negation=True
                )
            ]
        )

        return task.to_repr(), 200

    def post(self, task_id: str):
        # TODO check path parameter task_id
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
        except ValueError as v:
            logger.exception("Unable to build a Task from [%s]" % posted_data, exc_info=v)
            abort(400, message="Some fields contains invalid parameters")
            return
        except TypeError as t:
            logger.exception("Unable to build a Task from [%s]" % posted_data, exc_info=t)
            abort(400, message="Some fields contains invalid parameters")
            return

        logger.info("Created task [%s]" % task)
        return task.to_repr(), 200

    def put(self, task_id: str):
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
        except ValueError as v:
            logger.exception("Unable to build a Task from [%s]" % posted_data, exc_info=v)
            abort(400, message="Some fields contains invalid parameters")
            return
        except TypeError as t:
            logger.exception("Unable to build a Task from [%s]" % posted_data, exc_info=t)
            abort(400, message="Some fields contains invalid parameters")
            return

        logger.info("Updated task [%s]" % task)
        return task.to_repr(), 200

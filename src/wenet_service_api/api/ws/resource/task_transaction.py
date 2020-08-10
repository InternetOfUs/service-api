from __future__ import absolute_import, annotations

from flask import request

import logging

from flask_restful import abort

from wenet.common.model.task.transaction import TaskTransaction
from wenet_service_api.common.exception.exceptions import NotAuthorized, BadRequestException
from wenet_service_api.connector.collector import ServiceConnectorCollector
from wenet_service_api.api.ws.resource.common import AuthenticatedResource, WenetSource
from wenet_service_api.dao.dao_collector import DaoCollector

logger = logging.getLogger("api.api.ws.resource.task_transaction")


class TaskTransactionInterfaceBuilder:

    @staticmethod
    def routes(service_connector_collector: ServiceConnectorCollector, authorized_apikey: str, dao_collector: DaoCollector):
        return [
            (TaskTransactionInterface, "", (service_connector_collector, authorized_apikey, dao_collector))
        ]


class TaskTransactionInterface(AuthenticatedResource):

    def __init__(self, service_connector_collector: ServiceConnectorCollector, authorized_apikey: str, dao_collector: DaoCollector) -> None:
        super().__init__(authorized_apikey, dao_collector)
        self.service_connector_collector = service_connector_collector

    def post(self):

        # TODO check source
        self._check_authentication([WenetSource.COMPONENT, WenetSource.APP, WenetSource.OAUTH2_AUTHORIZATION_CODE])

        try:
            posted_data: dict = request.get_json()
        except Exception as e:
            logger.exception("Invalid message body", exc_info=e)
            abort(400, message="Invalid JSON - Unable to parse message body")
            return

        try:
            task_transaction = TaskTransaction.from_repr(posted_data)
        except (ValueError, TypeError) as v:
            logger.exception(f"Unable to build a TaskTransaction from [{posted_data}]", exc_info=v)
            abort(400, message="Some fields contains invalid parameters")
            return
        except KeyError as k:
            logger.exception(f"Unable to build a TaskTransaction from [{posted_data}]", exc_info=k)
            abort(400, message=f"The field [{k}] is missing")
            return

        logger.info(f"Received TaskTransaction {task_transaction}")

        try:
            self.service_connector_collector.task_manager_connector.post_task_transaction(task_transaction)
        except NotAuthorized as n:
            logger.exception(f"User unauthorized to post the task transaction", exc_info=n)
        except BadRequestException as e:
            logger.exception(f"Bad request exception during creation of task transaction[{task_transaction}]", exc_info=e)
            abort(400, message=str(e))
            return
        except Exception as e:
            logger.exception(f"Unable to create the task transaction [{task_transaction}]", exc_info=e)
            abort(500, message="Unable to create the task transaction")
            return

        logger.info(f"Posted TaskTransaction {task_transaction}")

        return {}, 201

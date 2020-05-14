from __future__ import absolute_import, annotations

from flask import request

import logging

from flask_restful import abort

from wenet.common.model.task.transaction import TaskTransaction
from wenet_service_api.connector.collector import ServiceConnectorCollector
from wenet_service_api.api.ws.resource.common import AuthenticatedResource
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

        self._check_authentication()

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

        return {}, 201

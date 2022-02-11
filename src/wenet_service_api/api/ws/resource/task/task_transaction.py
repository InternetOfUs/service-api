from __future__ import absolute_import, annotations

from typing import Optional

from flask import request

import logging

from flask_restful import abort
from wenet.interface.exceptions import BadRequest

from wenet.model.task.transaction import TaskTransaction
from wenet_service_api.connector.collector import ServiceConnectorCollector
from wenet_service_api.api.ws.resource.common import AuthenticatedResource, WenetSource

logger = logging.getLogger("api.api.ws.resource.task_transaction")


class TaskTransactionInterfaceBuilder:

    @staticmethod
    def routes(service_connector_collector: ServiceConnectorCollector, authorized_apikey: str):
        return [
            (TaskTransactionInterface, "", (service_connector_collector, authorized_apikey))
        ]


class TaskTransactionInterface(AuthenticatedResource):

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
            task_transaction = TaskTransaction.from_repr(posted_data)
        except (ValueError, TypeError):
            logger.info(f"Unable to build a TaskTransaction from [{posted_data}]")
            abort(400, message="Unable to build a TaskTransactions")
            return
        except KeyError as k:
            logger.info(f"Unable to build a TaskTransaction from [{posted_data}]")
            abort(400, message=f"The field [{k}] is missing")
            return

        logger.info(f"Received TaskTransaction {task_transaction}")

        try:
            self._service_connector_collector.task_manager_connector.create_task_transaction(task_transaction)
        except BadRequest as e:
            logger.info(f"Unable to store a task transaction, server replay with [{e.http_status_code}] [{e.server_response}]")
            return self.build_api_exception_response(e)
        except Exception as e:
            logger.exception(f"Unable to create the task transaction [{task_transaction}]", exc_info=e)
            abort(500, message="Unable to create the task transaction")
            return

        logger.info(f"Posted TaskTransaction {task_transaction}")

        return {}, 201

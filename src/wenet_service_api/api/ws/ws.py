from __future__ import absolute_import, annotations

from flask import Flask
from flask_restful import Api

import logging

from wenet_service_api.api.ws.resource.logging import MessageLoggingInterfaceBuilder
from wenet_service_api.api.ws.resource.task.task_list import TaskListResourceInterfaceBuilder
from wenet_service_api.api.ws.resource.token_deatils import TokenDetailsInterfaceBuilder
from wenet_service_api.api.ws.resource.user.builder import WeNetUserProfileInterfaceBuilder
from wenet_service_api.connector.collector import ServiceConnectorCollector
from wenet_service_api.api.ws.resource.app import AppResourceInterfaceBuilder
from wenet_service_api.api.ws.resource.task.task import TaskResourceInterfaceBuilder
from wenet_service_api.api.ws.resource.task.task_transaction import TaskTransactionInterfaceBuilder


class WsInterface:

    def __init__(self, service_connector_collector: ServiceConnectorCollector, authorized_apikey: str) -> None:
        self._app = Flask("api")
        self._api = Api(app=self._app)

        self._authorized_api_key = authorized_apikey

        self._init_modules(service_connector_collector)

    def _init_modules(self, service_connector_collector: ServiceConnectorCollector) -> None:
        active_routes = [
            (WeNetUserProfileInterfaceBuilder.routes(service_connector_collector, self._authorized_api_key), "/user"),
            (TaskResourceInterfaceBuilder.routes(service_connector_collector, self._authorized_api_key), "/task"),
            (TaskTransactionInterfaceBuilder.routes(service_connector_collector, self._authorized_api_key), "/task/transaction"),
            (AppResourceInterfaceBuilder.routes(service_connector_collector, self._authorized_api_key), "/app"),
            (TaskListResourceInterfaceBuilder.routes(service_connector_collector, self._authorized_api_key), "/tasks"),
            (TokenDetailsInterfaceBuilder.routes(service_connector_collector, self._authorized_api_key), "/token"),
            (MessageLoggingInterfaceBuilder.routes(service_connector_collector, self._authorized_api_key), "/log")
        ]

        for module_routes, prefix in active_routes:
            for resource, path, args in module_routes:
                logging.debug("Installing route %s", prefix + path)
                self._api.add_resource(resource, prefix + path, resource_class_args=args)

    def run_server(self, host: str = "0.0.0.0", port: int = 80, debug=False):
        self._app.run(host=host, port=port, debug=debug)

    def get_application(self):
        return self._app

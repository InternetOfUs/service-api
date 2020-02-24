from __future__ import absolute_import, annotations

from flask import Flask
from flask_restful import Api

import logging

from wenet.wenet_service_api.ws.resource.message_interface import MessageInterfaceBuilder
from wenet.wenet_service_api.ws.resource.task_interface import TaskResourceInterfaceBuilder
from wenet.wenet_service_api.ws.resource.user_profile import WeNetUserProfileInterfaceBuilder


class WsInterface:

    def __init__(self) -> None:
        self._app = Flask("wenet_service_api")
        self._api = Api(app=self._app)
        self._init_modules()

    def _init_modules(self) -> None:
        active_routes = [
            (WeNetUserProfileInterfaceBuilder.routes(), "/user"),
            (TaskResourceInterfaceBuilder.routes(), "/task"),
            (MessageInterfaceBuilder.routes(), "/messages")
        ]

        for module_routes, prefix in active_routes:
            for resource, path, args in module_routes:
                logging.debug("Installing route %s", prefix + path)
                self._api.add_resource(resource, prefix + path, resource_class_args=args)

    def run_server(self, host: str = "0.0.0.0", port: int = 80, debug=False):
        self._app.run(host=host, port=port, debug=debug)

    def get_application(self):
        return self._app

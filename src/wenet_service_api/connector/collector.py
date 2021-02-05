from __future__ import absolute_import, annotations

import os
import logging

from wenet_service_api.connector.hub_connector import HubConnector, DummyHubConnector
from wenet_service_api.connector.logger_connectory import LoggerConnector, DummyLoggerConnector
from wenet_service_api.connector.profile_manager import ProfileManagerConnector, DummyProfileManagerConnector
from wenet_service_api.connector.task_manager import TaskManagerConnector, DummyTaskManagerConnector

logger = logging.getLogger("api.api.connector")


class ServiceConnectorCollector:

    def __init__(self,
                 profile_manager_collector: ProfileManagerConnector,
                 task_manager_connector: TaskManagerConnector,
                 hub_connector: HubConnector,
                 logger_connector: LoggerConnector
                 ):
        self.profile_manager_collector = profile_manager_collector
        self.task_manager_connector = task_manager_connector
        self.hub_connector = hub_connector
        self.logger_connector = logger_connector

    @staticmethod
    def build() -> ServiceConnectorCollector:

        component_apikey = os.getenv("COMP_AUTH_KEY", None)
        component_apikey_header = os.getenv("COMP_AUTH_KEY_HEADER", "x-wenet-component-apikey")

        if component_apikey is not None:
            headers = {
                component_apikey_header: component_apikey
            }
        else:
            headers = {}

        if os.getenv("DEBUG", None):
            logger.info("Using dummy connectors")
            return ServiceConnectorCollector(
                profile_manager_collector=DummyProfileManagerConnector.build_from_env(headers),
                task_manager_connector=DummyTaskManagerConnector.build_from_env(headers),
                hub_connector=DummyHubConnector.build_from_env(headers),
                logger_connector=DummyLoggerConnector.build_from_env(headers)
            )
        else:
            return ServiceConnectorCollector(
                profile_manager_collector=ProfileManagerConnector.build_from_env(headers),
                task_manager_connector=TaskManagerConnector.build_from_env(headers),
                hub_connector=HubConnector.build_from_env(headers),
                logger_connector=LoggerConnector.build_from_env(headers)
            )

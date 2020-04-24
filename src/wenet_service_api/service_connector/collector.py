from __future__ import absolute_import, annotations

import os
import logging

from wenet_service_api.service_connector.profile_manager_connector import ProfileManagerConnector, DummyProfileManagerConnector
from wenet_service_api.service_connector.task_manager_connector import TaskManagerConnector, DummyTaskManagerConnector

logger = logging.getLogger("api.api.service_connector")


class ServiceConnectorCollector:

    def __init__(self, profile_manager_collector: ProfileManagerConnector, task_manager_connector: TaskManagerConnector):
        self.profile_manager_collector = profile_manager_collector
        self.task_manager_connector = task_manager_connector

    @staticmethod
    def build() -> ServiceConnectorCollector:

        if os.getenv("DEBUG", None):
            logger.info("Using dummy connectors")
            return ServiceConnectorCollector(
                profile_manager_collector=DummyProfileManagerConnector.build_from_env(),
                task_manager_connector=DummyTaskManagerConnector.build_from_env()
            )
        else:
            return ServiceConnectorCollector(
                profile_manager_collector=ProfileManagerConnector.build_from_env(),
                task_manager_connector=TaskManagerConnector.build_from_env()
            )

from __future__ import absolute_import, annotations

import os
import logging

from wenet.interface.profile_manager import ProfileManagerInterface
from wenet.interface.task_manager import TaskManagerInterface
from wenet.interface.hub import HubInterface
from wenet.interface.logger import LoggerInterface
from wenet.interface.client import ApikeyClient

logger = logging.getLogger("api.api.connector")


class ServiceConnectorCollector:

    def __init__(self,
                 profile_manager_collector: ProfileManagerInterface,
                 task_manager_connector: TaskManagerInterface,
                 hub_connector: HubInterface,
                 logger_connector: LoggerInterface
                 ):
        self.profile_manager_collector = profile_manager_collector
        self.task_manager_connector = task_manager_connector
        self.hub_connector = hub_connector
        self.logger_connector = logger_connector

    @staticmethod
    def build() -> ServiceConnectorCollector:

        component_apikey = os.getenv("COMP_AUTH_KEY", None)
        component_apikey_header = os.getenv("COMP_AUTH_KEY_HEADER", "x-wenet-component-apikey")

        client = ApikeyClient(component_apikey, component_apikey_header)

        base_url = os.getenv("PLATFORM_BASE_URL")

        return ServiceConnectorCollector(
            profile_manager_collector=ProfileManagerInterface(client=client, platform_url=base_url),
            task_manager_connector=TaskManagerInterface(client=client, platform_url=base_url),
            hub_connector=HubInterface(client=client, platform_url=base_url),
            logger_connector=LoggerInterface(client=client, platform_url=base_url)
        )

from __future__ import absolute_import, annotations

from wenet_service_api.connector.collector import ServiceConnectorCollector

from wenet.interface.profile_manager import ProfileManagerInterface
from wenet.interface.task_manager import TaskManagerInterface
from wenet.interface.hub import HubInterface
from wenet.interface.logger import LoggerInterface
from wenet.interface.client import NoAuthenticationClient


class MockServiceConnectorCollector(ServiceConnectorCollector):

    @staticmethod
    def build() -> ServiceConnectorCollector:
        return ServiceConnectorCollector(
            profile_manager_collector=ProfileManagerInterface(NoAuthenticationClient(), ""),
            task_manager_connector=TaskManagerInterface(NoAuthenticationClient(), ""),
            hub_connector=HubInterface(NoAuthenticationClient(), ""),
            logger_connector=LoggerInterface(NoAuthenticationClient(), "")
        )

from __future__ import absolute_import, annotations

from wenet_service_api.connector.collector import ServiceConnectorCollector
from wenet_service_api.connector.hub_connector import HubConnector
from wenet_service_api.connector.profile_manager import ProfileManagerConnector
from wenet_service_api.connector.task_manager import TaskManagerConnector


class MockServiceConnectorCollector(ServiceConnectorCollector):

    @staticmethod
    def build() -> ServiceConnectorCollector:
        return ServiceConnectorCollector(
            profile_manager_collector=ProfileManagerConnector(""),
            task_manager_connector=TaskManagerConnector(""),
            hub_connector=HubConnector("")
        )

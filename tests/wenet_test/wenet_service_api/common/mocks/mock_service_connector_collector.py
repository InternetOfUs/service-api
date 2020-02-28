from __future__ import absolute_import, annotations

from wenet.service_connector.collector import ServiceConnectorCollector
from wenet.service_connector.profile_manager_connector import ProfileManagerConnector
from wenet.service_connector.task_manager_connector import TaskManagerConnector


class MockServiceConnectorCollector(ServiceConnectorCollector):

    @staticmethod
    def build() -> ServiceConnectorCollector:
        return ServiceConnectorCollector(
            profile_manager_collector=ProfileManagerConnector(""),
            task_manager_connector=TaskManagerConnector("")
        )

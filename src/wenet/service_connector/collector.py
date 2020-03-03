from __future__ import absolute_import, annotations

from wenet.service_connector.profile_manager_connector import ProfileManagerConnector
from wenet.service_connector.task_manager_connector import TaskManagerConnector


class ServiceConnectorCollector:

    def __init__(self, profile_manager_collector: ProfileManagerConnector, task_manager_connector: TaskManagerConnector):
        self.profile_manager_collector = profile_manager_collector
        self.task_manager_connector = task_manager_connector

    @staticmethod
    def build() -> ServiceConnectorCollector:
        return ServiceConnectorCollector(
            profile_manager_collector=ProfileManagerConnector.build_from_env(),
            task_manager_connector=TaskManagerConnector.build_from_env()
        )

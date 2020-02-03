from __future__ import absolute_import, annotations

from wenet.service_connector.profile_manager import ProfileManagerConnector


class ServiceConnectorCollector:

    def __init__(self, profile_manager_collector: ProfileManagerConnector):
        self.profile_manager_collector = profile_manager_collector

    @staticmethod
    def build() -> ServiceConnectorCollector:
        return ServiceConnectorCollector(
            profile_manager_collector=ProfileManagerConnector.build_from_env()
        )

from __future__ import absolute_import, annotations

import logging

from wenet_service_api.api.ws.resource.user.competences import WeNetUserCompetencesInterface
from wenet_service_api.api.ws.resource.user.core_profile import WeNetUserCoreProfileInterface
from wenet_service_api.api.ws.resource.user.materials import WeNetUserMaterialsInterface
from wenet_service_api.connector.collector import ServiceConnectorCollector

logger = logging.getLogger("api.api.ws.resource.user.builder")


class WeNetUserProfileInterfaceBuilder:

    @staticmethod
    def routes(service_connector_collector: ServiceConnectorCollector, authorized_apikey: str):
        return [
            (WeNetUserCoreProfileInterface, "/profile/<string:profile_id>", (service_connector_collector, authorized_apikey)),
            (WeNetUserCompetencesInterface, "/profile/<string:profile_id>/competences", (service_connector_collector, authorized_apikey)),
            (WeNetUserMaterialsInterface, "/profile/<string:profile_id>/materials", (service_connector_collector, authorized_apikey)),
        ]

from __future__ import absolute_import, annotations

from wenet_service_api.api.ws.resource.user.competences import WeNetUserCompetencesInterface
from wenet_service_api.api.ws.resource.user.core_profile import WeNetUserCoreProfileInterface
from wenet_service_api.api.ws.resource.user.materials import WeNetUserMaterialsInterface
from wenet_service_api.api.ws.resource.user.meanings import WeNetUserMeaningsInterface
from wenet_service_api.api.ws.resource.user.norms import WeNetUserNormsInterface
from wenet_service_api.api.ws.resource.user.personal_behaviors import WeNetUserPersonalBehaviorsInterface
from wenet_service_api.api.ws.resource.user.planned_activities import WeNetUserPlannedActivitiesInterface
from wenet_service_api.api.ws.resource.user.relationships import WeNetUserRelationshipsInterface
from wenet_service_api.api.ws.resource.user.relevant_locations import WeNetUserRelevantLocationsInterface
from wenet_service_api.connector.collector import ServiceConnectorCollector


class WeNetUserProfileInterfaceBuilder:

    @staticmethod
    def routes(service_connector_collector: ServiceConnectorCollector, authorized_apikey: str):
        return [
            (WeNetUserCoreProfileInterface, "/profile/<string:profile_id>", (service_connector_collector, authorized_apikey)),
            (WeNetUserCompetencesInterface, "/profile/<string:profile_id>/competences", (service_connector_collector, authorized_apikey)),
            (WeNetUserMaterialsInterface, "/profile/<string:profile_id>/materials", (service_connector_collector, authorized_apikey)),
            (WeNetUserMeaningsInterface, "/profile/<string:profile_id>/meanings", (service_connector_collector, authorized_apikey)),
            (WeNetUserNormsInterface, "/profile/<string:profile_id>/norms", (service_connector_collector, authorized_apikey)),
            (WeNetUserPersonalBehaviorsInterface, "/profile/<string:profile_id>/personalBehaviors", (service_connector_collector, authorized_apikey)),
            (WeNetUserPlannedActivitiesInterface, "/profile/<string:profile_id>/plannedActivities", (service_connector_collector, authorized_apikey)),
            (WeNetUserRelationshipsInterface, "/profile/<string:profile_id>/relationships", (service_connector_collector, authorized_apikey)),
            (WeNetUserRelevantLocationsInterface, "/profile/<string:profile_id>/relevantLocations", (service_connector_collector, authorized_apikey))
        ]

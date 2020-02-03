from __future__ import absolute_import, annotations

from datetime import datetime

from flask import request
from flask_restful import Resource, abort

import logging

from wenet.common.exception.excpetions import ResourceNotFound
from wenet.model.user_profile import WeNetUserProfile
from wenet.service_connector.collector import ServiceConnectorCollector

logger = logging.getLogger("wenet.wenet_service_api.ws.resource.wenet_user_profile")


class WeNetUserProfileInterfaceBuilder:

    @staticmethod
    def routes(service_connector_collector: ServiceConnectorCollector):
        return [
            (WeNetUserProfileInterface, "/profile/<string:profile_id>", (service_connector_collector,))
        ]


class WeNetUserProfileInterface(Resource):

    def __init__(self, service_connector_collector: ServiceConnectorCollector) -> None:
        super().__init__()
        self._service_connector_collector = service_connector_collector

    def get(self, profile_id: str):

        try:
            profile = self._service_connector_collector.profile_manager_collector.get_profile(profile_id)
        except ResourceNotFound as e:
            logger.exception("Unable to retrieve the profile", exc_info=e)
            abort(404, message="Resource not found")
            return
        except Exception as e:
            logger.exception("Unable to retrieve the profile", exc_info=e)
            abort(500)
            return
        return profile.to_repr(), 200

    def put(self, profile_id: str):

        try:
            posted_data: dict = request.get_json()
        except Exception as e:
            logger.exception("Invalid message body", exc_info=e)
            abort(400, message="Invalid JSON - Unable to parse message body")
            return

        try:
            user_profile = WeNetUserProfile.from_repr(posted_data, profile_id)
        except (ValueError, TypeError) as v:
            logger.exception("Unable to build a WeNetUserProfile from [%s]" % posted_data, exc_info=v)
            abort(400, message="Some fields contains invalid parameters")
            return
        except KeyError as k:
            logger.exception("Unable to build a WeNetUserProfile from [%s]" % posted_data, exc_info=k)
            abort(400, message="The field [%s] is missing" % k)
            return

        logger.info("updated profile [%s]" % user_profile)

        try:
            self._service_connector_collector.profile_manager_collector.update_profile(user_profile)
            logger.info("Profile [%s] updated successfully" % profile_id)
        except ResourceNotFound as e:
            logger.exception("Unable to retrieve the profile", exc_info=e)
            abort(404, message="Resource not found")
            return
        except Exception as e:
            logger.exception("Unable to retrieve the profile", exc_info=e)
            abort(500)
            return

        return user_profile.to_repr(), 200

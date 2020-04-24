from __future__ import absolute_import, annotations

from flask import request
from flask_restful import abort

import logging

from wenet_service_api.service_common.exception.exceptions import ResourceNotFound, NotAuthorized, BadRequestException
from wenet_service_api.service_connector.collector import ServiceConnectorCollector
from wenet.service_api.user_profile import CoreWeNetUserProfile
from wenet_service_api.api.ws.resource.common import AuthenticatedResource

logger = logging.getLogger("api.api.ws.resource.wenet_user_profile")


class WeNetUserProfileInterfaceBuilder:

    @staticmethod
    def routes(service_connector_collector: ServiceConnectorCollector, authorized_apikey: str):
        return [
            (WeNetUserProfileInterface, "/profile/<string:profile_id>", (service_connector_collector, authorized_apikey))
        ]


class WeNetUserProfileInterface(AuthenticatedResource):

    def __init__(self, service_connector_collector: ServiceConnectorCollector, authorized_apikey: str) -> None:
        super().__init__(authorized_apikey)
        self._service_connector_collector = service_connector_collector

    def get(self, profile_id: str):

        self._check_authentication()

        try:
            profile = self._service_connector_collector.profile_manager_collector.get_profile(profile_id)
            logger.info(f"Retrieved profile [{profile_id}] from profile manager connector")
        except ResourceNotFound as e:
            logger.exception("Unable to retrieve the profile", exc_info=e)
            abort(404, message="Resource not found")
            return
        except NotAuthorized as e:
            logger.exception(f"Unauthorized to retrieve the task [{profile_id}]", exc_info=e)
            abort(403)
            return
        except Exception as e:
            logger.exception("Unable to retrieve the profile", exc_info=e)
            abort(500)
            return
        return profile.to_repr(), 200

    def put(self, profile_id: str):

        self._check_authentication()

        try:
            posted_data: dict = request.get_json()
        except Exception as e:
            logger.exception("Invalid message body", exc_info=e)
            abort(400, message="Invalid JSON - Unable to parse message body")
            return

        try:
            user_profile = CoreWeNetUserProfile.from_repr(posted_data, profile_id)
        except (ValueError, TypeError) as v:
            logger.exception("Unable to build a WeNetUserProfile from [%s]" % posted_data, exc_info=v)
            abort(400, message="Some fields contains invalid parameters")
            return
        except KeyError as k:
            logger.exception("Unable to build a WeNetUserProfile from [%s]" % posted_data, exc_info=k)
            abort(400, message="The field [%s] is missing" % k)
            return

        try:
            stored_user_profile = self._service_connector_collector.profile_manager_collector.get_profile(profile_id)
            logger.info(f"Retrieved profile [{profile_id}] from profile manager connector")
        except ResourceNotFound as e:
            logger.exception("Unable to retrieve the profile", exc_info=e)
            abort(404, message="Resource not found")
            return
        except NotAuthorized as e:
            logger.exception(f"Unauthorized to retrieve the task [{profile_id}]", exc_info=e)
            abort(403)
            return
        except Exception as e:
            logger.exception("Unable to retrieve the profile", exc_info=e)
            abort(500)
            return

        stored_user_profile.update(user_profile)

        logger.info("updating profile [%s]" % stored_user_profile)

        try:
            self._service_connector_collector.profile_manager_collector.update_profile(stored_user_profile)
            logger.info("Profile [%s] updated successfully" % profile_id)
        except ResourceNotFound as e:
            logger.exception("Unable to retrieve the profile", exc_info=e)
            abort(404, message="Resource not found")
            return
        except BadRequestException as e:
            logger.exception(f"Bad request during update of profile [{profile_id}][{user_profile}] - [{str(e)}")
            abort(400, message=f"Bad request: {str(e)}")
            return
        except Exception as e:
            logger.exception("Unable to retrieve the profile", exc_info=e)
            abort(500)
            return

        return {}, 200

    def post(self, profile_id: str):
        self._check_authentication()

        try:
            user_profile = self._service_connector_collector.profile_manager_collector.create_empty_profile(profile_id)
        except BadRequestException as e:
            logger.exception(f"Bad request during profile creation [{str(e)}")
            abort(400, message=f"Bad request: {str(e)}")
            return
        except Exception as e:
            logger.exception("Unable to create the profile", exc_info=e)
            abort(500)
            return

        logger.info(f"Created empty profile [{user_profile}]")

        return {}, 200

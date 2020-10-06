from __future__ import absolute_import, annotations

from flask import request
from flask_restful import abort

import logging

from wenet.common.model.user.user_profile import CoreWeNetUserProfile, WeNetUserProfile
from wenet_service_api.common.exception.exceptions import ResourceNotFound, NotAuthorized, BadRequestException
from wenet_service_api.connector.collector import ServiceConnectorCollector
from wenet_service_api.api.ws.resource.common import AuthenticatedResource, WenetSource, AuthenticationResult, \
    Oauth2Result, Scope, ComponentAuthentication

logger = logging.getLogger("api.api.ws.resource.wenet_user_profile")


class WeNetUserProfileInterfaceBuilder:

    @staticmethod
    def routes(service_connector_collector: ServiceConnectorCollector, authorized_apikey: str):
        return [
            (WeNetUserProfileInterface, "/profile/<string:profile_id>", (service_connector_collector, authorized_apikey))
        ]


class WeNetUserProfileInterface(AuthenticatedResource):

    def __init__(self, service_connector_collector: ServiceConnectorCollector, authorized_apikey: str) -> None:
        super().__init__(authorized_apikey, service_connector_collector)

    @staticmethod
    def _get_user_id(authentication_result: AuthenticationResult) -> str:

        if isinstance(authentication_result, Oauth2Result):
            return authentication_result.wenet_user_id
        else:
            profile_id = request.headers.get("X-Wenet-Userid")
            if profile_id is None or profile_id == "":
                abort(400, message="missing X-Wenet-Userid header")
                return
            else:
                return profile_id

    def _can_view_profile(self, authentication_result: AuthenticationResult, profile_id: str) -> bool:
        if isinstance(authentication_result, ComponentAuthentication):
            return True
        elif isinstance(authentication_result, Oauth2Result):
            try:
                user_ids = self._service_connector_collector.hub_connector.get_app_users(app_id=authentication_result.app.app_id)
                return profile_id in user_ids
            except ResourceNotFound:
                return False
        else:
            return False

    @staticmethod
    def _can_edit_profile(authentication_result, profile_id: str) -> bool:
        if isinstance(authentication_result, ComponentAuthentication):
            return True
        elif isinstance(authentication_result, Oauth2Result):
            return authentication_result.wenet_user_id == profile_id
        else:
            return False

    def get(self, profile_id: str):

        authentication_result = self._check_authentication([WenetSource.COMPONENT, WenetSource.OAUTH2_AUTHORIZATION_CODE])

        if not self._can_view_profile(authentication_result, profile_id):
            abort(401)
            return

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

        if isinstance(authentication_result, ComponentAuthentication):
            return profile.to_repr(), 200
        elif isinstance(authentication_result, Oauth2Result):
            return profile.to_filtered_repr(authentication_result.scopes), 200
        else:
            logger.error(f"Unable to handle authentication of type {type(authentication_result)}")
            abort(500)
            return

    def put(self, profile_id: str):

        authentication_result = self._check_authentication([WenetSource.COMPONENT, WenetSource.OAUTH2_AUTHORIZATION_CODE])

        if not self._can_edit_profile(authentication_result, profile_id):
            abort(401)
            return

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

        stored_user_profile = self._update_user_profile(user_profile, stored_user_profile, authentication_result)

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

    def post(self, profile_id):
        self._check_authentication([WenetSource.COMPONENT])

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

    @staticmethod
    def _update_user_profile(user_profile: CoreWeNetUserProfile, stored_user_profile: WeNetUserProfile, authentication_result: AuthenticationResult) -> WeNetUserProfile:
        if not isinstance(authentication_result, Oauth2Result):
            stored_user_profile.update(user_profile)
            return stored_user_profile
        else:
            if not authentication_result.has_scope(Scope.ID):
                stored_user_profile.profile_id = None

            if user_profile.name is not None:
                if authentication_result.has_scope(Scope.FIRST_NAME):
                    stored_user_profile.name.first = user_profile.name.first
                if authentication_result.has_scope(Scope.MIDDLE_NAME):
                    stored_user_profile.name.middle = user_profile.name.middle
                if authentication_result.has_scope(Scope.LAST_NAME):
                    stored_user_profile.name.last = user_profile.name.last
                if authentication_result.has_scope(Scope.PREFIX_NAME):
                    stored_user_profile.name.prefix = user_profile.name.prefix
                if authentication_result.has_scope(Scope.SUFFIX_NAME):
                    stored_user_profile.name.suffix = user_profile.name.suffix
            else:
                if authentication_result.has_scope(Scope.FIRST_NAME):
                    user_profile.name.first = None
                if authentication_result.has_scope(Scope.MIDDLE_NAME):
                    user_profile.name.middle = None
                if authentication_result.has_scope(Scope.LAST_NAME):
                    user_profile.name.last = None
                if authentication_result.has_scope(Scope.PREFIX_NAME):
                    user_profile.name.prefix = None
                if authentication_result.has_scope(Scope.SUFFIX_NAME):
                    user_profile.name.suffix = None

            if authentication_result.has_scope(Scope.BIRTHDATE):
                stored_user_profile.date_of_birth = user_profile.date_of_birth
            if authentication_result.has_scope(Scope.GENDER):
                stored_user_profile.gender = user_profile.gender
            if authentication_result.has_scope(Scope.EMAIL):
                stored_user_profile.email = user_profile.email
            if authentication_result.has_scope(Scope.PHONE_NUMBER):
                stored_user_profile.phone_number = user_profile.phone_number
            if authentication_result.has_scope(Scope.LOCALE):
                stored_user_profile.locale = user_profile.locale
            if authentication_result.has_scope(Scope.NATIONALITY):
                stored_user_profile.nationality = user_profile.nationality

            return stored_user_profile

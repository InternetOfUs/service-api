from __future__ import absolute_import, annotations

from flask import request
from flask_restful import abort

import logging

from wenet.interface.exceptions import AuthenticationException, NotFound
from wenet.model.user.profile import CoreWeNetUserProfile, WeNetUserProfile

from wenet_service_api.api.ws.resource.user.common import CommonWeNetUserInterface
from wenet_service_api.api.ws.resource.common import WenetSource, AuthenticationResult, Oauth2Result, Scope, ComponentAuthentication

logger = logging.getLogger("api.api.ws.resource.user.core_profile")


class WeNetUserCoreProfileInterface(CommonWeNetUserInterface):

    def get(self, profile_id: str):

        authentication_result = self._check_authentication([WenetSource.COMPONENT, WenetSource.OAUTH2_AUTHORIZATION_CODE])

        if not self._can_view_profile(authentication_result, profile_id):
            abort(401)
            return

        try:
            profile = self._service_connector_collector.profile_manager_collector.get_user_profile(profile_id)
            logger.info(f"Retrieved profile [{profile_id}] from profile manager connector")
        except NotFound as e:
            logger.exception("Unable to retrieve the profile", exc_info=e)
            abort(404, message="Resource not found")
            return
        except AuthenticationException as e:
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
            if self._is_owner(authentication_result, profile_id):
                return profile.to_filtered_repr(authentication_result.scopes), 200
            else:
                return profile.to_public_repr(), 200
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
            stored_user_profile = self._service_connector_collector.profile_manager_collector.get_user_profile(profile_id)
            logger.info(f"Retrieved profile [{profile_id}] from profile manager connector")
        except NotFound as e:
            logger.exception("Unable to retrieve the profile", exc_info=e)
            abort(404, message="Resource not found")
            return
        except AuthenticationException as e:
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
            updated_profile = self._service_connector_collector.profile_manager_collector.update_user_profile(stored_user_profile)
            logger.info("Profile [%s] updated successfully" % profile_id)
        except AuthenticationException as e:
            logger.exception(f"Unauthorized to update the profile [{profile_id}]", exc_info=e)
            abort(403)
            return
        # except ResourceNotFound as e:
        #     logger.exception("Unable to retrieve the profile [{profile_id}]", exc_info=e)
        #     abort(404, message="Resource not found")
        #     return
        # except BadRequestException as e:
        #     logger.exception(f"Bad request during update of profile [{profile_id}][{user_profile}] - [{str(e)}")
        #     abort(400, message=f"Bad request: {str(e)}")
        #     return
        except Exception as e:
            logger.exception("Unable to retrieve the profile", exc_info=e)
            abort(500)
            return

        if isinstance(authentication_result, ComponentAuthentication):
            return updated_profile.to_repr(), 200
        elif isinstance(authentication_result, Oauth2Result):
            if self._is_owner(authentication_result, profile_id):
                return updated_profile.to_filtered_repr(authentication_result.scopes), 200
            else:
                return updated_profile.to_public_repr(), 200
        else:
            logger.error(f"Unable to handle authentication of type {type(authentication_result)}")
            abort(500)
            return

    def post(self, profile_id):
        self._check_authentication([WenetSource.COMPONENT])

        try:
            user_profile = self._service_connector_collector.profile_manager_collector.create_empty_user_profile(profile_id)
        except AuthenticationException as e:
            logger.exception(f"Unauthorized to create the profile [{profile_id}]", exc_info=e)
            abort(403)
            return
        # except BadRequestException as e:
        #     logger.exception(f"Bad request during profile creation [{str(e)}")
        #     abort(400, message=f"Bad request: {str(e)}")
        #     return
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

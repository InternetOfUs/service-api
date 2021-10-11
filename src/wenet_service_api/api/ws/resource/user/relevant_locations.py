from __future__ import absolute_import, annotations

from flask import request
from flask_restful import abort

import logging

from wenet.interface.exceptions import NotFound, AuthenticationException
from wenet.model.user.profile import PatchWeNetUserProfile

from wenet_service_api.api.ws.resource.user.common import CommonWeNetUserInterface
from wenet_service_api.api.ws.resource.common import WenetSource, Oauth2Result, ComponentAuthentication

logger = logging.getLogger("api.api.ws.resource.user.relevant_locations")


class WeNetUserRelevantLocationsInterface(CommonWeNetUserInterface):

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
            logger.exception(f"Unauthorized to retrieve the profile [{profile_id}]", exc_info=e)
            abort(403)
            return
        except Exception as e:
            logger.exception("Unable to retrieve the profile", exc_info=e)
            abort(500)
            return

        if isinstance(authentication_result, ComponentAuthentication):
            return profile.relevant_locations, 200
        elif isinstance(authentication_result, Oauth2Result):
            if self._is_owner(authentication_result, profile_id):  # and authentication_result.has_scope(Scope.RELEVANT_LOCATIONS):  # TODO check for the reading scope when will be added
                return profile.relevant_locations, 200
            else:
                abort(403)
                return
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
            posted_relevant_locations: list = request.get_json()
        except Exception as e:
            logger.exception("Invalid message body", exc_info=e)
            abort(400, message="Invalid JSON - Unable to parse message body")
            return

        logger.info("Updating relevant locations [%s]" % posted_relevant_locations)

        patched_profile = PatchWeNetUserProfile(profile_id=profile_id, relevant_locations=posted_relevant_locations)

        try:
            if not isinstance(authentication_result, Oauth2Result):
                updated_profile = self._service_connector_collector.profile_manager_collector.patch_user_profile(patched_profile)
            else:
                # if authentication_result.has_scope(Scope.RELEVANT_LOCATIONS):  # TODO check for the writing scope when will be added
                updated_profile = self._service_connector_collector.profile_manager_collector.patch_user_profile(patched_profile)
                # else:
                #     abort(403)
                #     return
            logger.info("Updated successfully relevant locations [%s]" % updated_profile.relevant_locations)
        except AuthenticationException as e:
            logger.exception(f"Unauthorized to update the relevant locations of the profile [{profile_id}]", exc_info=e)
            abort(403)
            return
        # except NotFound as e:
        #     logger.exception(f"Unable to find the profile [{profile_id}]", exc_info=e)
        #     abort(404, message="Resource not found")
        #     return
        # except BadRequestException as e:
        #     logger.exception(f"Bad request during update of profile [{profile_id}] - [{str(e)}")
        #     abort(400, message=f"Bad request: {str(e)}")
        #     return
        except Exception as e:
            logger.exception("Unable to update the profile", exc_info=e)
            abort(500)
            return

        if isinstance(authentication_result, ComponentAuthentication):
            return updated_profile.relevant_locations, 200
        elif isinstance(authentication_result, Oauth2Result):
            if self._is_owner(authentication_result, profile_id):  # and authentication_result.has_scope(Scope.RELEVANT_LOCATIONS):  # TODO check for the reading scope when will be added
                return updated_profile.relevant_locations, 200
            else:
                return [], 200
        else:
            logger.error(f"Unable to handle authentication of type {type(authentication_result)}")
            abort(500)
            return

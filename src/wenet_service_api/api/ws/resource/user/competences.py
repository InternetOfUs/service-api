from __future__ import absolute_import, annotations

from flask import request
from flask_restful import abort

import logging

from wenet.interface.exceptions import NotFound, AuthenticationException
from wenet.model.user.profile import PatchWeNetUserProfile

from wenet_service_api.api.ws.resource.user.common import CommonWeNetUserInterface
from wenet_service_api.api.ws.resource.common import WenetSource, Oauth2Result, ComponentAuthentication

logger = logging.getLogger("api.api.ws.resource.user.competences")


class WeNetUserCompetencesInterface(CommonWeNetUserInterface):

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
            return profile.competences, 200
        elif isinstance(authentication_result, Oauth2Result):
            if self._is_owner(authentication_result, profile_id):  # and authentication_result.has_scope(Scope.ID):  # TODO check for the reading scope when will be added
                return profile.competences, 200
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
            posted_competences: list = request.get_json()
        except Exception as e:
            logger.exception("Invalid message body", exc_info=e)
            abort(400, message="Invalid JSON - Unable to parse message body")
            return

        logger.info("Updating competences [%s]" % posted_competences)

        try:
            if not isinstance(authentication_result, Oauth2Result):
                updated_competences = self._service_connector_collector.profile_manager_collector.patch_user_profile(PatchWeNetUserProfile(profile_id=profile_id, competences=posted_competences))
            else:
                # if authentication_result.has_scope(Scope.ID):  # TODO check for the writing scope when will be added
                updated_competences = self._service_connector_collector.profile_manager_collector.patch_user_profile(PatchWeNetUserProfile(profile_id=profile_id, competences=posted_competences))
            logger.info("Updated successfully competences [%s]" % updated_competences)
        except AuthenticationException as e:
            logger.exception(f"Unauthorized to update the competences of the profile [{profile_id}]", exc_info=e)
            abort(403)
            return
        # except ResourceNotFound as e:
        #     logger.exception(f"Unable to find the profile [{profile_id}]", exc_info=e)
        #     abort(404, message="Resource not found")
        #     return
        # except BadRequestException as e:
        #     logger.exception(f"Bad request during update of profile [{profile_id}] - [{str(e)}")
        #     abort(400, message=f"Bad request: {str(e)}")
        #     return
        except Exception as e:
            logger.exception("Unable to retrieve the profile", exc_info=e)
            abort(500)
            return

        if isinstance(authentication_result, ComponentAuthentication):
            return updated_competences, 200
        elif isinstance(authentication_result, Oauth2Result):  # and authentication_result.has_scope(Scope.ID):  # TODO check for the reading scope when will be added
            if self._is_owner(authentication_result, profile_id):
                return updated_competences, 200
            else:
                return [], 200
        else:
            logger.error(f"Unable to handle authentication of type {type(authentication_result)}")
            abort(500)
            return

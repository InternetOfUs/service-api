from __future__ import absolute_import, annotations

from flask import request
from flask_restful import abort

import logging

from wenet.interface.exceptions import NotFound, BadRequest
from wenet.model.user.profile import PatchWeNetUserProfile

from wenet_service_api.api.ws.resource.user.common import CommonWeNetUserInterface
from wenet_service_api.api.ws.resource.common import WenetSource, Oauth2Result, ComponentAuthentication, Scope

logger = logging.getLogger("api.api.ws.resource.user.norms")


class WeNetUserNormsInterface(CommonWeNetUserInterface):

    def get(self, profile_id: str):

        authentication_result = self._check_authentication([WenetSource.COMPONENT, WenetSource.OAUTH2_AUTHORIZATION_CODE])

        if isinstance(authentication_result, Oauth2Result):
            if not self._is_owner(authentication_result, profile_id):
                abort(403, message=f"Unauthorized to retrieve the profile [{profile_id}]")
                return
            if Scope.NORMS_READ not in authentication_result.scopes:
                abort(403, message="Unauthorized to read the user norms")
                return

        try:
            profile = self._service_connector_collector.profile_manager_collector.get_user_profile(profile_id)
            logger.info(f"Retrieved profile [{profile_id}] from profile manager connector")
        except (NotFound, BadRequest) as e:
            logger.info(f"Unable to retrieve the profile with id [{profile_id}], server replay with [{e.http_status_code}] [{e.server_response}]")
            return self.build_api_exception_response(e)
        except Exception as e:
            logger.exception("Unable to retrieve the profile", exc_info=e)
            abort(500)
            return

        return profile.norms, 200

    def put(self, profile_id: str):

        authentication_result = self._check_authentication([WenetSource.COMPONENT, WenetSource.OAUTH2_AUTHORIZATION_CODE])

        if not self._can_edit_profile(authentication_result, profile_id):
            abort(401)
            return

        if isinstance(authentication_result, Oauth2Result):
            if Scope.NORMS_WRITE not in authentication_result.scopes:
                abort(403, message="Unauthorized to write the user norms")
                return

        # Will raise a BadRequest if an invalid json is provided with the ContentType application/json. None with a different ContentType
        posted_norms = request.get_json()

        if posted_norms is None:
            abort(400, message="The body should be a json object")
            return

        logger.info("Updating norms [%s]" % posted_norms)

        try:
            patched_profile = PatchWeNetUserProfile(profile_id=profile_id, norms=posted_norms)
        except TypeError:
            logger.info(f"Unable to build a patch for the wenet profile from [{posted_norms}]")
            abort(400, message="Invalid data")
            return

        try:
            updated_profile = self._service_connector_collector.profile_manager_collector.patch_user_profile(patched_profile)
            logger.info("Updated successfully norms [%s]" % updated_profile.norms)
        except (NotFound, BadRequest) as e:
            logger.info(f"Unauthorized to update the norms of the profile [{profile_id}], server replay with [{e.http_status_code}] [{e.server_response}]")
            return self.build_api_exception_response(e)
        except Exception as e:
            logger.exception("Unable to update the profile", exc_info=e)
            abort(500)
            return

        if isinstance(authentication_result, ComponentAuthentication):
            return updated_profile.norms, 200
        elif isinstance(authentication_result, Oauth2Result):
            if self._is_owner(authentication_result, profile_id) and authentication_result.has_scope(Scope.NORMS_READ):
                return updated_profile.norms, 200
            else:
                return [], 200
        else:
            logger.error(f"Unable to handle authentication of type {type(authentication_result)}")
            abort(500)
            return

from __future__ import absolute_import, annotations

import logging
from typing import Optional, List

from flask import request
from flask_restful import abort, reqparse
from wenet.interface.exceptions import NotFound, AuthenticationException, BadRequest
from wenet.model.user.relationship import Relationship

from wenet_service_api.api.ws.resource.common import WenetSource, Oauth2Result, ComponentAuthentication, Scope
from wenet_service_api.api.ws.resource.user.common import CommonWeNetUserInterface

logger = logging.getLogger("api.api.ws.resource.user.relationships")


class WeNetUserRelationshipsInterface(CommonWeNetUserInterface):

    def get(self, profile_id: str):

        authentication_result = self._check_authentication([WenetSource.COMPONENT, WenetSource.OAUTH2_AUTHORIZATION_CODE])

        parser = reqparse.RequestParser()
        parser.add_argument("offset", type=int, required=False, help="The index of the first social network relationship to return.")
        parser.add_argument("limit", type=int, required=False, help="The number maximum of social network relationships to return")

        parser.add_argument("targetId", type=str, required=False, help="A user identifier to be equals on the relationships target to return. You can use a Perl compatible regular expressions (PCRE) that has to match the user identifier of the relationships target if you write between '/'. For example to get the relationships with the target users '1' and '2' you must pass as 'target' '/^[1|2]$/'.")
        parser.add_argument("type", type=str, required=False, help="The number maximum of social network relationships to return")
        parser.add_argument("weightFrom", type=float, required=False, help="The minimal weight, inclusive, of the relationships to return.")
        parser.add_argument("weightTo", type=float, required=False, help="The maximal weight, inclusive, of the relationships to return.")
        parser.add_argument("order", type=str, required=False, help="The order in witch the relationships has to be returned. For each field it has be separated by a ',' and each field can start with '+' (or without it) to order on ascending order, or with the prefix '-' to do on descendant order. Example : sourceId,-weight,+type")
        args = parser.parse_args()

        if isinstance(authentication_result, Oauth2Result):
            if not self._is_owner(authentication_result, profile_id):
                abort(403, message=f"Unauthorized to retrieve the profile [{profile_id}]")
                return
            if Scope.RELATIONSHIPS_READ not in authentication_result.scopes:
                abort(403, message="Unauthorized to read the user relationship")
                return
            app_id = authentication_result.app.app_id
        else:
            app_id = None

        try:
            relationship_page = self._service_connector_collector.profile_manager_collector.get_relationship_page(
                app_id=app_id,
                source_id=profile_id,
                target_id=args.get("targetId"),
                relation_type=args.get("type"),
                weight_from=args.get("weightFrom"),
                weight_to=args.get("weightTo"),
                order=args.get("order"),
                offset=args.get("offset", 0),
                limit=args.get("limit", 10)
            )
            logger.info(f"Retrieved the relationships for profile [{profile_id}] from profile manager connector")
        except (NotFound, BadRequest) as e:
            logger.info(f"Unable to retrieve the relationships for the profile with id [{profile_id}], server replay with [{e.http_status_code}] [{e.server_response}]")
            return self.build_api_exception_response(e)
        except Exception as e:
            logger.exception(f"Unable to retrieve the user relationship for user [{profile_id}]", exc_info=e)
            abort(500)
            return

        return relationship_page.to_repr(), 200

    def put(self, profile_id: str):

        authentication_result = self._check_authentication([WenetSource.COMPONENT, WenetSource.OAUTH2_AUTHORIZATION_CODE])

        if not self._can_edit_profile(authentication_result, profile_id):
            abort(401)
            return

        if isinstance(authentication_result, Oauth2Result):
            if Scope.RELATIONSHIPS_WRITE not in authentication_result.scopes:
                abort(403, message="Unauthorized to write the user relationships")
                return

        # Will raise a BadRequest if an invalid json is provided with the ContentType application/json. None with a different ContentType
        raw_posted_relationships: Optional[List[dict]] = request.get_json()

        if raw_posted_relationships is None:
            abort(400, message="The body should be a json object")
            return

        posted_relationships = [Relationship.from_repr(x) for x in raw_posted_relationships]

        if isinstance(authentication_result, Oauth2Result):
            for relationship in posted_relationships:
                if relationship.source_id != authentication_result.wenet_user_id:
                    abort(403, message="Unable to write a relationship for a different user profile")
                    return

        logger.info(f"Updating relationships for user [{profile_id}]")

        try:
            updated_relationship = self._service_connector_collector.profile_manager_collector.update_relationship_batch(posted_relationships)

            logger.info(f"Updated successfully relationships for user [{profile_id}]")
        except AuthenticationException as e:
            logger.info(f"Unable to update the relationships of the profile [{profile_id}], server replay with [{e.http_status_code}] [{e.server_response}]")
            return self.build_api_exception_response(e)
        except Exception as e:
            logger.exception(f"Unable to update the relationships of the profile [{profile_id}]", exc_info=e)
            abort(500)
            return

        if isinstance(authentication_result, ComponentAuthentication):
            return [x.to_repr() for x in updated_relationship], 200
        elif isinstance(authentication_result, Oauth2Result):
            if self._is_owner(authentication_result, profile_id) and authentication_result.has_scope(Scope.RELATIONSHIPS_READ):
                return [x.to_repr() for x in updated_relationship], 200
            else:
                return [], 200
        else:
            logger.error(f"Unable to handle authentication of type {type(authentication_result)}")
            abort(500)
            return

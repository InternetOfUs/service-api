from __future__ import absolute_import, annotations

from datetime import datetime

from flask import request
from flask_restful import Resource, abort

import logging

from wenet.model.common import Gender, UserLanguage, Date
from wenet.model.user_profile import WeNetUserProfile, UserName
from wenet.wenet_service_api.ws.resource.common import AuthenticatedResource

logger = logging.getLogger("wenet.wenet_service_api.ws.resource.wenet_user_profile")


class WeNetUserProfileInterfaceBuilder:

    @staticmethod
    def routes(authorized_apikey: str):
        return [
            (WeNetUserProfileInterface, "/profile/<string:profile_id>", (authorized_apikey,))
        ]


class WeNetUserProfileInterface(AuthenticatedResource):

    def __init__(self, authorized_apikey: str) -> None:
        super().__init__(authorized_apikey)

    def get(self, profile_id: str):

        self._check_authentication()

        user_profile = WeNetUserProfile(
            name=UserName(
                first="John",
                middle="Francis",
                last="Doe",
                prefix="Dr.",
                suffix="Jr."
            ),
            date_of_birth=Date(
                year=1976,
                month=4,
                day=23
            ),
            gender=Gender.MALE,
            email="john.doe@gmail.com",
            phone_number="+34 6888233133",
            locale="es_ES",
            avatar="avatar",
            nationality="Spanish",
            languages=[
                UserLanguage(
                    name="Spanish",
                    level="C2",
                    code="es"
                )
            ],
            occupation="nurse",
            creation_ts=datetime(2020, 1, 21).timestamp(),
            last_update_ts=datetime.now().timestamp(),
            profile_id=profile_id,
            norms=[],
            planned_activities=[],
            relevant_locations=[],
            relationships=[],
            social_practices=[],
            personal_behaviours=[]
        )

        return user_profile.to_repr(), 200

    def put(self, profile_id: str):

        self._check_authentication()

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

        return user_profile.to_repr(), 200

from __future__ import absolute_import, annotations

from datetime import datetime

from flask import request
from flask_restful import Resource, abort

import logging

from wenet.model.common import Gender, UserLanguage, Date
from wenet.model.user_profile import WeNetUserProfile, UserName

logger = logging.getLogger("wenet.wenet_service_api.ws.resource.wenet_user_profile")


class WeNetUserProfileInterfaceBuilder:

    @staticmethod
    def routes():
        return [
            (WeNetUserProfileInterface, "/profile/<string:profile_id>", ())
        ]


class WeNetUserProfileInterface(Resource):

    def __init__(self) -> None:
        super().__init__()

    def get(self, profile_id: str):

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

        try:
            posted_data: dict = request.get_json()
        except Exception as e:
            logger.exception("Invalid message body", exc_info=e)
            abort(400, message="Invalid JSON - Unable to parse message body")
            return

        # remove id from body, the id in the path parameter is used
        posted_data["id"] = profile_id
        try:
            user_profile = WeNetUserProfile.from_repr(posted_data)
        except ValueError as v:
            logger.exception("Unable to build a WeNetUserProfile from [%s]" % posted_data, exc_info=v)
            abort(400, message="Some fields contains invalid parameters")
            return
        except TypeError as t:
            logger.exception("Unable to build a WeNetUserProfile from [%s]" % posted_data, exc_info=t)
            abort(400, message="Some fields contains invalid parameters")
            return

        logger.info("updated profile [%s]" % user_profile)

        return user_profile.to_repr(), 200

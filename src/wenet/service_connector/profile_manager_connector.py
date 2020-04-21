from __future__ import absolute_import, annotations

import json
import os
from typing import Optional

import requests

from wenet.service_common.exception.excpetions import ResourceNotFound, NotAuthorized, BadRequestException
from wenet.model.common import Date, Gender, UserLanguage
from wenet.model.norm import Norm, NormOperator
from wenet.model.user_profile import WeNetUserProfile, CoreWeNetUserProfile, UserName
from wenet.service_connector.service_connector import ServiceConnector


class ProfileManagerConnector(ServiceConnector):

    def __init__(self, base_url: str, base_headers: Optional[dict] = None):
        super().__init__(base_url, base_headers)

    @staticmethod
    def build_from_env() -> ProfileManagerConnector:

        base_url = os.getenv("PROFILE_MANAGER_CONNECTOR_BASE_URL")

        if not base_url:
            raise RuntimeError("ENV: PROFILE_MANAGER_CONNECTOR_BASE_URL is not defined")

        return ProfileManagerConnector(
            base_url=base_url,
            base_headers={
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
        )

    def get_profile(self, profile_id, headers: Optional[dict] = None) -> WeNetUserProfile:
        url = "%s/profiles/%s" % (self._base_url, profile_id)

        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = requests.get(url, headers=headers)

        if response.status_code == 200 or response.status_code == 202:
            return WeNetUserProfile.from_repr(response.json())
        elif response.status_code == 404:
            raise ResourceNotFound("Unable to found a profile with id [%s]" % profile_id)
        elif response.status_code == 401 or response.status_code == 403:
            raise NotAuthorized("Not authorized")
        elif response.status_code == 400:
            raise BadRequestException(f"Bad request: {response.text}")
        else:
            raise Exception("Unable to found a profile with id [%s], server respond [%s] [%s]" % (profile_id, response.status_code, response.text))

    def update_profile(self, profile: WeNetUserProfile, headers: Optional[dict] = None):
        url = "%s/profiles/%s" % (self._base_url, profile.profile_id)

        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        data_repr = self.prepare_profile(profile)
        data = json.dumps(data_repr)

        response = requests.put(url, data=data, headers=headers)
        if response.status_code == 200 or response.status_code == 202:
            # return WeNetUserProfile.from_repr(response.json())
            return
        elif response.status_code == 404:
            raise ResourceNotFound("Unable to found a profile with id [%s]" % profile.profile_id)
        elif response.status_code == 401 or response.status_code == 403:
            raise NotAuthorized("Not authorized")
        elif response.status_code == 400:
            raise BadRequestException(f"Bad request: {response.text}")
        else:
            raise Exception("Unable to edit the profile with id [%s], server respond [%s] [%s]" % (profile.profile_id, response.status_code, response.text))

    def create_empty_profile(self, wenet_user_id: str, headers: Optional[dict] = None) -> WeNetUserProfile:
        url = "%s/profiles" % self._base_url

        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        empty_profile = WeNetUserProfile.empty(wenet_user_id)
        data_repr = self.prepare_profile(empty_profile)
        data = json.dumps(data_repr)

        response = requests.post(url, data=data, headers=headers)
        if response.status_code == 200:
            return empty_profile  # TODO check
        elif response.status_code == 401 or response.status_code == 403:
            raise NotAuthorized("Not authorized")
        elif response.status_code == 400:
            raise BadRequestException(f"Bad request: {response.text}")
        else:
            raise Exception("Unable to create an empty profile")

    @staticmethod
    def prepare_profile(profile: WeNetUserProfile) -> dict:
        profile_repr = profile.to_repr()
        profile_repr.pop("_creationTs", None)
        profile_repr.pop("_lastUpdateTs", None)

        return profile_repr


class DummyProfileManagerConnector(ProfileManagerConnector):

    def __init__(self):
        super().__init__("", None)

    @staticmethod
    def build_from_env() -> ProfileManagerConnector:
        return DummyProfileManagerConnector()

    def get_profile(self, profile_id, headers: Optional[dict] = None) -> WeNetUserProfile:
        return WeNetUserProfile(
            name=UserName(
                first="first",
                middle="middle",
                last="last",
                prefix="prefix",
                suffix="suffix"
            ),
            date_of_birth=Date(
                year=2020,
                month=1,
                day=20
            ),
            gender=Gender.MALE,
            email="email@example.com",
            phone_number="phone number",
            locale="it_IT",
            avatar="avatar",
            nationality="it",
            languages=[
                UserLanguage(
                    name="ita",
                    level="C2",
                    code="it"
                )
            ],
            occupation="occupation",
            creation_ts=1579536160,
            last_update_ts=1579536160,
            profile_id=profile_id,
            norms=[
                Norm(
                    norm_id="norm-id",
                    attribute="attribute",
                    operator=NormOperator.EQUALS,
                    comparison=True,
                    negation=False
                )
            ],
            planned_activities=[],
            relevant_locations=[],
            relationships=[],
            social_practices=[],
            personal_behaviours=[]
        )

    def update_profile(self, profile: WeNetUserProfile, headers: Optional[dict] = None):
        return profile

    def create_empty_profile(self, wenet_user_id: str, headers: Optional[dict] = None) -> WeNetUserProfile:
        return WeNetUserProfile.empty(wenet_user_id)

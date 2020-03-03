from __future__ import absolute_import, annotations

import json

from tests.wenet_test.wenet_service_api.common.common_test_case import CommonTestCase
from wenet.model.common import Date, Gender, UserLanguage
from wenet.model.norm import Norm, NormOperator
from wenet.model.user_profile import WeNetUserProfile, UserName


class TestUser(CommonTestCase):

    def test_get(self):

        profile_id = "profile-id"
        response = self.client.get("/user/profile/%s" % profile_id, headers={"apikey": self.AUTHORIZED_APIKEY})
        self.assertEqual(response.status_code, 200)

        json_data = json.loads(response.data)

        user_profile = WeNetUserProfile.from_repr(json_data)

        self.assertIsInstance(user_profile, WeNetUserProfile)
        self.assertEqual(user_profile.profile_id, profile_id)

    def test_get_not_authorized(self):

        profile_id = "profile-id"
        response = self.client.get("/user/profile/%s" % profile_id)
        self.assertEqual(response.status_code, 403)

    def test_put(self):
        profile_id = "profile_id"
        user_profile = WeNetUserProfile(
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

        response = self.client.put("/user/profile/%s" % profile_id, json=user_profile.to_repr(), headers={"apikey": self.AUTHORIZED_APIKEY})
        self.assertEqual(200, response.status_code)
        json_response = json.loads(response.data)
        user_profile = WeNetUserProfile.from_repr(json_response)
        self.assertIsInstance(user_profile, WeNetUserProfile)

    def test_put_not_authorized(self):
        profile_id = "profile_id"
        user_profile = WeNetUserProfile(
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

        response = self.client.put("/user/profile/%s" % profile_id, json=user_profile.to_repr())
        self.assertEqual(403, response.status_code)

    def test_put2(self):
        profile_id = "profile_id"
        user_profile = {'name': {'first': 'first', 'middle': 'middle', 'last': 'last', 'prefix': 'prefix', 'suffix': 'suffix'}, 'gender': 'M', 'email': 'email@example.com', 'phoneNumber': 'phone number', 'locale': 'it_IT', 'avatar': 'avatar', 'nationality': 'it', 'languages': [{'name': 'ita', 'level': 'C2', 'code': 'it'}], 'occupation': 'occupation', '_creationTs': 1579536160, '_lastUpdateTs': 1579536160, 'id': 'profile_id', 'norms': [{'id': 'norm-id', 'attribute': 'attribute', 'operator': 'EQUALS', 'comparison': True, 'negation': False}], 'plannedActivities': [], 'relevantLocations': [], 'relationships': [], 'socialPractices': [], 'personalBehaviors': []}

        response = self.client.put("/user/profile/<string:profile_id>", json=user_profile, headers={"apikey": self.AUTHORIZED_APIKEY})
        self.assertEqual(400, response.status_code)

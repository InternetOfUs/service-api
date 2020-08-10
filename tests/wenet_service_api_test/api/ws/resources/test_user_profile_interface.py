from __future__ import absolute_import, annotations

import json
from copy import deepcopy

from mock import Mock

from tests.wenet_service_api_test.api.common.common_test_case import CommonTestCase
from wenet.common.model.norm.norm import Norm, NormOperator
from wenet.common.model.user.common import Date, Gender, UserLanguage
from wenet.common.model.user.user_profile import WeNetUserProfile, UserName
from wenet_service_api.api.ws.resource.common import WenetSource, Scope


class TestUser(CommonTestCase):

    def test_get(self):
        profile_id = "profile-id"
        profile = WeNetUserProfile(
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

        mock_get = Mock(return_value=profile)
        self.service_collector_connector.profile_manager_collector.get_profile = mock_get

        response = self.client.get("/user/profile", headers={"apikey": self.AUTHORIZED_APIKEY, "x-wenet-source": WenetSource.COMPONENT.value, "X-Wenet-Userid": profile_id})
        self.assertEqual(response.status_code, 200)

        json_data = json.loads(response.data)

        user_profile = WeNetUserProfile.from_repr(json_data)

        self.assertIsInstance(user_profile, WeNetUserProfile)
        self.assertEqual(user_profile.profile_id, profile_id)
        self.assertEqual(profile, user_profile)
        mock_get.assert_called_once()

    def test_get_oauth(self):
        profile_id = "profile-id"
        profile = WeNetUserProfile(
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

        mock_get = Mock(return_value=deepcopy(profile))
        self.service_collector_connector.profile_manager_collector.get_profile = mock_get

        response = self.client.get("/user/profile", headers={
            "apikey": self.AUTHORIZED_APIKEY,
            "x-wenet-source": WenetSource.OAUTH2_AUTHORIZATION_CODE.value,
            "X-Authenticated-Scope": f"{Scope.ID.value} {Scope.FIRST_NAME.value}",
            "X-Authenticated-Userid": profile_id
        })
        self.assertEqual(200, response.status_code)

        json_data = json.loads(response.data)

        user_profile = WeNetUserProfile.from_repr(json_data)

        self.assertIsInstance(user_profile, WeNetUserProfile)
        self.assertEqual(user_profile.profile_id, profile_id)
        self.assertNotEqual(profile, user_profile)

        self.assertIsNotNone(user_profile.profile_id)
        self.assertIsNotNone(user_profile.name.first)
        self.assertIsNone(user_profile.name.last)
        self.assertIsNone(user_profile.name.middle)
        self.assertIsNone(user_profile.name.prefix)
        self.assertIsNone(user_profile.name.suffix)
        self.assertIsNone(user_profile.gender)
        self.assertIsNone(user_profile.email)
        self.assertIsNone(user_profile.phone_number)
        self.assertIsNone(user_profile.locale)
        self.assertIsNone(user_profile.nationality)
        self.assertIsNone(user_profile.date_of_birth)
        mock_get.assert_called_once()

    def test_get_not_authorized(self):

        response = self.client.get("/user/profile")
        self.assertEqual(response.status_code, 401)

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

        mock_put = Mock(return_value=None)
        self.service_collector_connector.profile_manager_collector.update_profile = mock_put

        mock_get = Mock(return_value=deepcopy(user_profile))
        self.service_collector_connector.profile_manager_collector.get_profile = mock_get

        response = self.client.put("/user/profile", json=user_profile.to_repr(), headers={"apikey": self.AUTHORIZED_APIKEY, "x-wenet-source": WenetSource.COMPONENT.value, "X-Wenet-Userid": profile_id})
        self.assertEqual(200, response.status_code)
        # json_response = json.loads(response.data)
        # user_profile = WeNetUserProfile.from_repr(json_response)
        # self.assertIsInstance(user_profile, WeNetUserProfile)
        mock_put.assert_called_once()
        mock_get.assert_called_once()

    def test_put_oauth2(self):
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

        mock_put = Mock(return_value=None)
        self.service_collector_connector.profile_manager_collector.update_profile = mock_put

        mock_get = Mock(return_value=deepcopy(user_profile))
        self.service_collector_connector.profile_manager_collector.get_profile = mock_get

        response = self.client.put("/user/profile", json=user_profile.to_repr(), headers={
            "apikey": self.AUTHORIZED_APIKEY,
            "x-wenet-source": WenetSource.OAUTH2_AUTHORIZATION_CODE.value,
            "X-Authenticated-Scope": f"{Scope.ID.value} {Scope.FIRST_NAME.value}",
            "X-Authenticated-Userid": profile_id
        })
        self.assertEqual(200, response.status_code)

        mock_put.assert_called_once()
        mock_get.assert_called_once()

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

        response = self.client.put("/user/profile", json=user_profile.to_repr())
        self.assertEqual(401, response.status_code)

    def test_put2(self):
        mock_put = Mock(return_value=None)
        self.service_collector_connector.profile_manager_collector.update_profile = mock_put
        
        user_profile = {'name': {'first': 'first', 'middle': 'middle', 'last': 'last', 'prefix': 'prefix', 'suffix': 'suffix'}, 'gender': 'M', 'email': 'email@example.com', 'phoneNumber': 'phone number', 'locale': 'it_IT', 'avatar': 'avatar', 'nationality': 'it', 'languages': [{'name': 'ita', 'level': 'C2', 'code': 'it'}], 'occupation': 'occupation', '_creationTs': 1579536160, '_lastUpdateTs': 1579536160, 'id': 'profile_id', 'norms': [{'id': 'norm-id', 'attribute': 'attribute', 'operator': 'EQUALS', 'comparison': True, 'negation': False}], 'plannedActivities': [], 'relevantLocations': [], 'relationships': [], 'socialPractices': [], 'personalBehaviors': []}

        mock_get = Mock(return_value=WeNetUserProfile.from_repr(user_profile))
        self.service_collector_connector.profile_manager_collector.get_profile = mock_get

        response = self.client.put("/user/profile", json=user_profile, headers={"apikey": self.AUTHORIZED_APIKEY, "x-wenet-source": WenetSource.COMPONENT.value, "X-Wenet-Userid": "profile_id"})
        self.assertEqual(200, response.status_code)

        mock_put.assert_called_once()
        mock_get.assert_called_once()

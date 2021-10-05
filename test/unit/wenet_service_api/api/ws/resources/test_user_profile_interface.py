from __future__ import absolute_import, annotations

import json
from copy import deepcopy
from datetime import datetime

from mock import Mock

from wenet.model.app import App, AppStatus
from wenet.model.norm import Norm, NormOperator
from wenet.model.user.common import Date, Gender
from wenet.model.user.profile import WeNetUserProfile, UserName

from test.unit.wenet_service_api.api.common.common_test_case import CommonTestCase
from wenet_service_api.api.ws.resource.common import WenetSource, Scope


class TestUser(CommonTestCase):
    app = App(
        app_id="1",
        status=AppStatus.STATUS_ACTIVE,
        message_callback_url="url",
        metadata={},
        creation_ts=int(datetime(2020, 2, 27).timestamp()),
        last_update_ts=int(datetime(2020, 2, 27).timestamp()),
        image_url="url",
        name="app_name",
        owner_id=1
    )

    app1 = App(
        app_id="2",
        status=AppStatus.STATUS_NOT_ACTIVE,
        message_callback_url="url",
        metadata={},
        creation_ts=int(datetime(2020, 2, 27).timestamp()),
        last_update_ts=int(datetime(2020, 2, 27).timestamp()),
        image_url="url",
        name="app_name",
        owner_id=1
    )

    developer_lis = ["1"]
    user_list = ["1", "11"]

    def setUp(self) -> None:
        super().setUp()

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
            personal_behaviours=[],
            materials=[],
            competences=[],
            meanings=[]
        )

        mock_get = Mock(return_value=profile)
        self.service_collector_connector.profile_manager_collector.get_user_profile = mock_get

        response = self.client.get("/user/profile/profile-id", headers={"apikey": self.AUTHORIZED_APIKEY, "x-wenet-source": WenetSource.COMPONENT.value})
        self.assertEqual(response.status_code, 200)

        json_data = json.loads(response.data)

        user_profile = WeNetUserProfile.from_repr(json_data)

        self.assertIsInstance(user_profile, WeNetUserProfile)
        self.assertEqual(user_profile.profile_id, profile_id)
        self.assertEqual(profile, user_profile)
        mock_get.assert_called_once()

    def test_get_oauth(self):
        profile_id = "1"
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
            personal_behaviours=[],
            materials=[],
            competences=[],
            meanings=[]
        )

        mock_get = Mock(return_value=deepcopy(profile))
        self.service_collector_connector.hub_connector.get_app_details = Mock(return_value=self.app)
        self.service_collector_connector.profile_manager_collector.get_user_profile = mock_get
        self.service_collector_connector.hub_connector.get_user_ids_for_app = Mock(return_value=self.user_list)

        response = self.client.get("/user/profile/1", headers={
            "apikey": self.AUTHORIZED_APIKEY,
            "x-wenet-source": WenetSource.OAUTH2_AUTHORIZATION_CODE.value,
            "X-Authenticated-Scope": f"{Scope.ID.value} {Scope.FIRST_NAME.value}",
            "X-Authenticated-Userid": profile_id,
            "X-Consumer-Username": "app_1"
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
        self.service_collector_connector.hub_connector.get_app_details.assert_called_once()

    def test_get_oauth_public_profile(self):
        profile_id = "1"
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
            personal_behaviours=[],
            materials=[],
            competences=[],
            meanings=[]
        )

        mock_get = Mock(return_value=deepcopy(profile))
        self.service_collector_connector.hub_connector.get_app_details = Mock(return_value=self.app)
        self.service_collector_connector.profile_manager_collector.get_user_profile = mock_get
        self.service_collector_connector.hub_connector.get_user_ids_for_app = Mock(return_value=self.user_list)

        response = self.client.get(f"/user/profile/{profile_id}", headers={
            "apikey": self.AUTHORIZED_APIKEY,
            "x-wenet-source": WenetSource.OAUTH2_AUTHORIZATION_CODE.value,
            "X-Authenticated-Scope": f"{Scope.ID.value} {Scope.FIRST_NAME.value} {Scope.LAST_NAME.value} {Scope.PHONE_NUMBER.value}",
            "X-Authenticated-Userid": "11",
            "X-Consumer-Username": "app_1"
        })
        self.assertEqual(200, response.status_code)

        json_data = json.loads(response.data)

        user_profile = WeNetUserProfile.from_repr(json_data)

        self.assertIsInstance(user_profile, WeNetUserProfile)
        self.assertEqual(user_profile.profile_id, "1")
        self.assertNotEqual(profile, user_profile)

        self.assertIsNotNone(user_profile.profile_id)
        self.assertIsNotNone(user_profile.name.first)
        self.assertIsNotNone(user_profile.name.last)
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
        self.service_collector_connector.hub_connector.get_app_details.assert_called_once()

    def test_get_oauth3(self):
        profile_id = "1"
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
            personal_behaviours=[],
            materials=[],
            competences=[],
            meanings=[]
        )

        mock_get = Mock(return_value=deepcopy(profile))
        self.service_collector_connector.profile_manager_collector.get_user_profile = mock_get
        self.service_collector_connector.hub_connector.get_app_details = Mock(return_value=self.app1)
        self.service_collector_connector.hub_connector.get_app_developers = Mock(return_value=self.developer_lis)
        self.service_collector_connector.hub_connector.get_user_ids_for_app = Mock(return_value=self.user_list)

        response = self.client.get(f"/user/profile/{profile_id}", headers={
            "apikey": self.AUTHORIZED_APIKEY,
            "x-wenet-source": WenetSource.OAUTH2_AUTHORIZATION_CODE.value,
            "X-Authenticated-Scope": f"{Scope.ID.value} {Scope.FIRST_NAME.value}",
            "X-Authenticated-Userid": profile_id,
            "X-Consumer-Username": "app_2"
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
        self.service_collector_connector.hub_connector.get_app_details.assert_called_once()
        self.service_collector_connector.hub_connector.get_app_developers.assert_called_once()
        self.service_collector_connector.hub_connector.get_user_ids_for_app.assert_called_once()

    def test_get_oauth4(self):
        profile_id = "2"
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
            personal_behaviours=[],
            materials=[],
            competences=[],
            meanings=[]
        )

        mock_get = Mock(return_value=deepcopy(profile))
        self.service_collector_connector.profile_manager_collector.get_user_profile = mock_get
        self.service_collector_connector.hub_connector.get_app_details = Mock(return_value=self.app1)
        self.service_collector_connector.hub_connector.get_app_developers = Mock(return_value=self.developer_lis)

        response = self.client.get(f"/user/profile/{profile_id}", headers={
            "apikey": self.AUTHORIZED_APIKEY,
            "x-wenet-source": WenetSource.OAUTH2_AUTHORIZATION_CODE.value,
            "X-Authenticated-Scope": f"{Scope.ID.value} {Scope.FIRST_NAME.value}",
            "X-Authenticated-Userid": profile_id,
            "X-Consumer-Username": "app_2"
        })
        self.assertEqual(403, response.status_code)

        self.service_collector_connector.hub_connector.get_app_details.assert_called_once()
        self.service_collector_connector.hub_connector.get_app_developers.assert_called_once()

    def test_get_not_authorized(self):

        response = self.client.get("/user/profile/1")
        self.assertEqual(response.status_code, 401)

    def test_put(self):
        profile_id = "1"
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
            personal_behaviours=[],
            materials=[],
            competences=[],
            meanings=[]
        )

        mock_put = Mock(return_value=None)
        self.service_collector_connector.profile_manager_collector.update_user_profile = mock_put

        mock_get = Mock(return_value=deepcopy(user_profile))
        self.service_collector_connector.profile_manager_collector.get_user_profile = mock_get

        response = self.client.put(f"/user/profile/{profile_id}", json=user_profile.to_repr(), headers={"apikey": self.AUTHORIZED_APIKEY, "x-wenet-source": WenetSource.COMPONENT.value})
        self.assertEqual(200, response.status_code)
        # json_response = json.loads(response.data)
        # user_profile = WeNetUserProfile.from_repr(json_response)
        # self.assertIsInstance(user_profile, WeNetUserProfile)
        mock_put.assert_called_once()
        mock_get.assert_called_once()

    def test_put_oauth2(self):
        profile_id = "1"
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
            personal_behaviours=[],
            materials=[],
            competences=[],
            meanings=[]
        )

        mock_put = Mock(return_value=None)
        self.service_collector_connector.profile_manager_collector.update_user_profile = mock_put
        self.service_collector_connector.hub_connector.get_app_details = Mock(return_value=self.app1)
        self.service_collector_connector.hub_connector.get_app_developers = Mock(return_value=self.developer_lis)

        mock_get = Mock(return_value=deepcopy(user_profile))
        self.service_collector_connector.profile_manager_collector.get_user_profile = mock_get

        response = self.client.put(f"/user/profile/{profile_id}", json=user_profile.to_repr(), headers={
            "apikey": self.AUTHORIZED_APIKEY,
            "x-wenet-source": WenetSource.OAUTH2_AUTHORIZATION_CODE.value,
            "X-Authenticated-Scope": f"{Scope.ID.value} {Scope.FIRST_NAME.value}",
            "X-Authenticated-Userid": profile_id,
            "X-Consumer-Username": "app_1"
        })
        self.assertEqual(200, response.status_code)

        mock_put.assert_called_once()
        mock_get.assert_called_once()
        self.service_collector_connector.hub_connector.get_app_details.assert_called_once()
        self.service_collector_connector.hub_connector.get_app_developers.assert_called_once()

    def test_put_oauth3(self):
        profile_id = "1"
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
            personal_behaviours=[],
            materials=[],
            competences=[],
            meanings=[]
        )

        mock_put = Mock(return_value=None)
        self.service_collector_connector.profile_manager_collector.update_user_profile = mock_put
        self.service_collector_connector.hub_connector.get_app_details = Mock(return_value=self.app1)
        self.service_collector_connector.hub_connector.get_app_developers = Mock(return_value=self.developer_lis)

        self.service_collector_connector.profile_manager_collector.get_profile = Mock(return_value=deepcopy(user_profile))

        response = self.client.put(f"/user/profile/2", json=user_profile.to_repr(), headers={
            "apikey": self.AUTHORIZED_APIKEY,
            "x-wenet-source": WenetSource.OAUTH2_AUTHORIZATION_CODE.value,
            "X-Authenticated-Scope": f"{Scope.ID.value} {Scope.FIRST_NAME.value}",
            "X-Authenticated-Userid": profile_id,
            "X-Consumer-Username": "app_1"
        })
        self.assertEqual(401, response.status_code)

        mock_put.assert_not_called()
        self.service_collector_connector.profile_manager_collector.get_profile.assert_not_called()
        self.service_collector_connector.hub_connector.get_app_details.assert_called_once()
        self.service_collector_connector.hub_connector.get_app_developers.assert_called_once()

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
            personal_behaviours=[],
            materials=[],
            competences=[],
            meanings=[]
        )

        response = self.client.put(f"/user/profile/{profile_id}", json=user_profile.to_repr())
        self.assertEqual(401, response.status_code)

    def test_put2(self):
        mock_put = Mock(return_value=None)
        self.service_collector_connector.profile_manager_collector.update_user_profile = mock_put

        user_profile = {'name': {'first': 'first', 'middle': 'middle', 'last': 'last', 'prefix': 'prefix', 'suffix': 'suffix'}, 'gender': 'M', 'email': 'email@example.com', 'phoneNumber': 'phone number', 'locale': 'it_IT', 'avatar': 'avatar', 'nationality': 'it', 'languages': [{'name': 'ita', 'level': 'C2', 'code': 'it'}], 'occupation': 'occupation', '_creationTs': 1579536160, '_lastUpdateTs': 1579536160, 'id': 'profile_id', 'norms': [{'id': 'norm-id', 'attribute': 'attribute', 'operator': 'EQUALS', 'comparison': True, 'negation': False}], 'plannedActivities': [], 'relevantLocations': [], 'relationships': [], 'socialPractices': [], 'personalBehaviors': []}

        mock_get = Mock(return_value=WeNetUserProfile.from_repr(user_profile))
        self.service_collector_connector.profile_manager_collector.get_user_profile = mock_get

        response = self.client.put("/user/profile/profile_id", json=user_profile, headers={"apikey": self.AUTHORIZED_APIKEY, "x-wenet-source": WenetSource.COMPONENT.value})
        self.assertEqual(200, response.status_code)

        mock_put.assert_called_once()
        mock_get.assert_called_once()

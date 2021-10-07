from __future__ import absolute_import, annotations

import json
from copy import deepcopy
from datetime import datetime

from mock import Mock

from wenet.model.app import App, AppStatus
from wenet.model.user.common import Date, Gender
from wenet.model.user.profile import WeNetUserProfile, UserName

from test.unit.wenet_service_api.api.common.common_test_case import CommonTestCase
from wenet_service_api.api.ws.resource.common import WenetSource, Scope


class TestWeNetUserCompetencesInterface(CommonTestCase):

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
            norms=[],
            planned_activities=[],
            relevant_locations=[],
            relationships=[],
            personal_behaviours=[],
            materials=[],
            competences=[
              {
                "name": "language_Italian_C1",
                "ontology": "esco",
                "level": 0.8
              }
            ],
            meanings=[]
        )

        mock_get = Mock(return_value=profile)
        self.service_collector_connector.profile_manager_collector.get_user_profile = mock_get

        response = self.client.get("/user/profile/profile-id/competences", headers={"apikey": self.AUTHORIZED_APIKEY, "x-wenet-source": WenetSource.COMPONENT.value})
        self.assertEqual(response.status_code, 200)

        json_data = json.loads(response.data)

        self.assertEqual(profile.competences, json_data)
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
            norms=[],
            planned_activities=[],
            relevant_locations=[],
            relationships=[],
            personal_behaviours=[],
            materials=[],
            competences=[
              {
                "name": "language_Italian_C1",
                "ontology": "esco",
                "level": 0.8
              }
            ],
            meanings=[]
        )

        mock_get = Mock(return_value=deepcopy(profile))
        self.service_collector_connector.hub_connector.get_app_details = Mock(return_value=self.app)
        self.service_collector_connector.profile_manager_collector.get_user_profile = mock_get
        self.service_collector_connector.hub_connector.get_user_ids_for_app = Mock(return_value=self.user_list)

        response = self.client.get("/user/profile/1/competences", headers={
            "apikey": self.AUTHORIZED_APIKEY,
            "x-wenet-source": WenetSource.OAUTH2_AUTHORIZATION_CODE.value,
            "X-Authenticated-Scope": f"{Scope.ID.value} {Scope.FIRST_NAME.value}",  # TODO add reading scope when will be added
            "X-Authenticated-Userid": profile_id,
            "X-Consumer-Username": "app_1"
        })
        self.assertEqual(200, response.status_code)

        json_data = json.loads(response.data)

        self.assertEqual(profile.competences, json_data)
        mock_get.assert_called_once()
        self.service_collector_connector.hub_connector.get_app_details.assert_called_once()

    def test_get_oauth_2(self):
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
            norms=[],
            planned_activities=[],
            relevant_locations=[],
            relationships=[],
            personal_behaviours=[],
            materials=[],
            competences=[
              {
                "name": "language_Italian_C1",
                "ontology": "esco",
                "level": 0.8
              }
            ],
            meanings=[]
        )

        mock_get = Mock(return_value=deepcopy(profile))
        self.service_collector_connector.profile_manager_collector.get_user_profile = mock_get
        self.service_collector_connector.hub_connector.get_app_details = Mock(return_value=self.app1)
        self.service_collector_connector.hub_connector.get_app_developers = Mock(return_value=self.developer_lis)

        response = self.client.get(f"/user/profile/{profile_id}/competences", headers={
            "apikey": self.AUTHORIZED_APIKEY,
            "x-wenet-source": WenetSource.OAUTH2_AUTHORIZATION_CODE.value,
            "X-Authenticated-Scope": f"{Scope.ID.value} {Scope.FIRST_NAME.value}",  # TODO add reading scope when will be added
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
        competences = [
          {
            "name": "language_Italian_C1",
            "ontology": "esco",
            "level": 0.8
          }
        ]

        mock_patch = Mock(return_value=competences)
        self.service_collector_connector.profile_manager_collector.patch_user_profile = mock_patch

        response = self.client.put(f"/user/profile/{profile_id}/competences", json=competences, headers={"apikey": self.AUTHORIZED_APIKEY, "x-wenet-source": WenetSource.COMPONENT.value})
        self.assertEqual(200, response.status_code)
        json_response = json.loads(response.data)
        self.assertEqual(competences, json_response)
        mock_patch.assert_called_once()

    def test_put_oauth(self):
        profile_id = "1"
        competences = [
            {
                "name": "language_Italian_C1",
                "ontology": "esco",
                "level": 0.8
            }
        ]

        mock_patch = Mock(return_value=competences)
        self.service_collector_connector.profile_manager_collector.patch_user_profile = mock_patch
        self.service_collector_connector.hub_connector.get_app_details = Mock(return_value=self.app1)
        self.service_collector_connector.hub_connector.get_app_developers = Mock(return_value=self.developer_lis)

        response = self.client.put(f"/user/profile/{profile_id}/competences", json=competences, headers={
            "apikey": self.AUTHORIZED_APIKEY,
            "x-wenet-source": WenetSource.OAUTH2_AUTHORIZATION_CODE.value,
            "X-Authenticated-Scope": f"{Scope.ID.value} {Scope.FIRST_NAME.value}",  # TODO add writing scope when will be added
            "X-Authenticated-Userid": profile_id,
            "X-Consumer-Username": "app_1"
        })
        self.assertEqual(200, response.status_code)
        json_response = json.loads(response.data)
        self.assertEqual(competences, json_response)

        mock_patch.assert_called_once()
        self.service_collector_connector.hub_connector.get_app_details.assert_called_once()
        self.service_collector_connector.hub_connector.get_app_developers.assert_called_once()

    def test_put_oauth_2(self):
        profile_id = "1"
        competences = [
            {
                "name": "language_Italian_C1",
                "ontology": "esco",
                "level": 0.8
            }
        ]

        mock_put = Mock(return_value=None)
        self.service_collector_connector.profile_manager_collector.update_user_profile = mock_put
        self.service_collector_connector.hub_connector.get_app_details = Mock(return_value=self.app1)
        self.service_collector_connector.hub_connector.get_app_developers = Mock(return_value=self.developer_lis)

        response = self.client.put(f"/user/profile/2/competences", json=competences, headers={
            "apikey": self.AUTHORIZED_APIKEY,
            "x-wenet-source": WenetSource.OAUTH2_AUTHORIZATION_CODE.value,
            "X-Authenticated-Scope": f"{Scope.ID.value} {Scope.FIRST_NAME.value}",  # TODO add writing scope when will be added
            "X-Authenticated-Userid": profile_id,
            "X-Consumer-Username": "app_1"
        })
        self.assertEqual(401, response.status_code)

        mock_put.assert_not_called()
        self.service_collector_connector.hub_connector.get_app_details.assert_called_once()
        self.service_collector_connector.hub_connector.get_app_developers.assert_called_once()

    def test_put_not_authorized(self):
        profile_id = "profile_id"
        competences = [
            {
                "name": "language_Italian_C1",
                "ontology": "esco",
                "level": 0.8
            }
        ]

        response = self.client.put(f"/user/profile/{profile_id}/competences", json=competences)
        self.assertEqual(401, response.status_code)

from __future__ import absolute_import, annotations

import json
from copy import deepcopy
from datetime import datetime

from mock import Mock

from wenet.model.app import App, AppStatus
from wenet.model.user.common import Date, Gender
from wenet.model.user.profile import WeNetUserProfile, UserName, PatchWeNetUserProfile

from test.unit.wenet_service_api.api.common.common_test_case import CommonTestCase
from wenet_service_api.api.ws.resource.common import WenetSource, Scope


class TestWeNetUserRelationshipsInterface(CommonTestCase):

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

    developer_list = ["1"]
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
            relationships=[
                {
                    "appId": "4",
                    "userId": "4c51ee0b-b7ec-4577-9b21-ae6832656e33",
                    "type": "friend",
                    "weight": 0.2
                }
            ],
            personal_behaviours=[],
            materials=[],
            competences=[],
            meanings=[]
        )

        mock_get = Mock(return_value=profile)
        self.service_collector_connector.profile_manager_collector.get_user_profile = mock_get

        response = self.client.get("/user/profile/profile-id/relationships", headers={"apikey": self.AUTHORIZED_APIKEY, "x-wenet-source": WenetSource.COMPONENT.value})
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.data)
        self.assertEqual(profile.relationships, json_data)
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
            relationships=[
                {
                    "appId": "4",
                    "userId": "4c51ee0b-b7ec-4577-9b21-ae6832656e33",
                    "type": "friend",
                    "weight": 0.2
                }
            ],
            personal_behaviours=[],
            materials=[],
            competences=[],
            meanings=[]
        )

        mock_get = Mock(return_value=deepcopy(profile))
        self.service_collector_connector.hub_connector.get_app_details = Mock(return_value=self.app)
        self.service_collector_connector.profile_manager_collector.get_user_profile = mock_get
        self.service_collector_connector.hub_connector.get_user_ids_for_app = Mock(return_value=self.user_list)

        response = self.client.get("/user/profile/1/relationships", headers={
            "apikey": self.AUTHORIZED_APIKEY,
            "x-wenet-source": WenetSource.OAUTH2_AUTHORIZATION_CODE.value,
            "X-Authenticated-Scope": f"{Scope.ID_READ.value} {Scope.FIRST_NAME_READ.value} {Scope.RELATIONSHIPS_READ.value}",
            "X-Authenticated-Userid": profile_id,
            "X-Consumer-Username": "app_1"
        })
        self.assertEqual(200, response.status_code)
        json_data = json.loads(response.data)
        self.assertEqual(profile.relationships, json_data)

        mock_get.assert_called_once()
        self.service_collector_connector.hub_connector.get_app_details.assert_called_once()
        self.service_collector_connector.hub_connector.get_user_ids_for_app.assert_not_called()

    def test_get_oauth_no_permission(self):
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
            relationships=[
                {
                    "appId": "4",
                    "userId": "4c51ee0b-b7ec-4577-9b21-ae6832656e33",
                    "type": "friend",
                    "weight": 0.2
                }
            ],
            personal_behaviours=[],
            materials=[],
            competences=[],
            meanings=[]
        )

        mock_get = Mock(return_value=deepcopy(profile))
        self.service_collector_connector.hub_connector.get_app_details = Mock(return_value=self.app)
        self.service_collector_connector.profile_manager_collector.get_user_profile = mock_get
        self.service_collector_connector.hub_connector.get_user_ids_for_app = Mock(return_value=self.user_list)

        response = self.client.get("/user/profile/1/relationships", headers={
            "apikey": self.AUTHORIZED_APIKEY,
            "x-wenet-source": WenetSource.OAUTH2_AUTHORIZATION_CODE.value,
            "X-Authenticated-Scope": f"{Scope.ID_READ.value} {Scope.FIRST_NAME_READ.value}",
            "X-Authenticated-Userid": profile_id,
            "X-Consumer-Username": "app_1"
        })
        self.assertEqual(403, response.status_code)

        mock_get.assert_not_called()
        self.service_collector_connector.hub_connector.get_app_details.assert_called_once()
        self.service_collector_connector.hub_connector.get_user_ids_for_app.assert_not_called()

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
            relationships=[
                {
                    "appId": "4",
                    "userId": "4c51ee0b-b7ec-4577-9b21-ae6832656e33",
                    "type": "friend",
                    "weight": 0.2
                }
            ],
            personal_behaviours=[],
            materials=[],
            competences=[],
            meanings=[]
        )

        mock_get = Mock(return_value=deepcopy(profile))
        self.service_collector_connector.profile_manager_collector.get_user_profile = mock_get
        self.service_collector_connector.hub_connector.get_app_details = Mock(return_value=self.app1)
        self.service_collector_connector.hub_connector.get_app_developers = Mock(return_value=self.developer_list)

        response = self.client.get(f"/user/profile/{profile_id}/relationships", headers={
            "apikey": self.AUTHORIZED_APIKEY,
            "x-wenet-source": WenetSource.OAUTH2_AUTHORIZATION_CODE.value,
            "X-Authenticated-Scope": f"{Scope.ID_READ.value} {Scope.FIRST_NAME_READ.value}",  # TODO add reading scope when will be added
            "X-Authenticated-Userid": profile_id,
            "X-Consumer-Username": "app_2"
        })
        self.assertEqual(403, response.status_code)

        mock_get.assert_not_called()
        self.service_collector_connector.hub_connector.get_app_details.assert_called_once()
        self.service_collector_connector.hub_connector.get_app_developers.assert_called_once()

    def test_get_not_authorized(self):
        mock_get = Mock(return_value=None)
        self.service_collector_connector.profile_manager_collector.get_user_profile = mock_get
        response = self.client.get("/user/profile/1/relationships")
        self.assertEqual(response.status_code, 401)
        mock_get.assert_not_called()

    def test_put(self):
        profile_id = "1"
        relationships = [
            {
                "appId": "4",
                "userId": "4c51ee0b-b7ec-4577-9b21-ae6832656e33",
                "type": "friend",
                "weight": 0.2
            }
        ]

        patched_profile = PatchWeNetUserProfile(profile_id=profile_id, relationships=relationships)

        mock_patch = Mock(return_value=patched_profile)
        self.service_collector_connector.profile_manager_collector.patch_user_profile = mock_patch

        response = self.client.put(f"/user/profile/{profile_id}/relationships", json=relationships, headers={"apikey": self.AUTHORIZED_APIKEY, "x-wenet-source": WenetSource.COMPONENT.value})
        self.assertEqual(200, response.status_code)
        json_response = json.loads(response.data)
        self.assertEqual(relationships, json_response)
        mock_patch.assert_called_once()

    def test_put_oauth(self):
        profile_id = "1"
        relationships = [
            {
                "appId": "4",
                "userId": "4c51ee0b-b7ec-4577-9b21-ae6832656e33",
                "type": "friend",
                "weight": 0.2
            }
        ]

        patched_profile = PatchWeNetUserProfile(profile_id=profile_id, relationships=relationships)

        mock_patch = Mock(return_value=patched_profile)
        self.service_collector_connector.profile_manager_collector.patch_user_profile = mock_patch
        self.service_collector_connector.hub_connector.get_app_details = Mock(return_value=self.app1)
        self.service_collector_connector.hub_connector.get_app_developers = Mock(return_value=self.developer_list)

        response = self.client.put(f"/user/profile/{profile_id}/relationships", json=relationships, headers={
            "apikey": self.AUTHORIZED_APIKEY,
            "x-wenet-source": WenetSource.OAUTH2_AUTHORIZATION_CODE.value,
            "X-Authenticated-Scope": f"{Scope.ID_READ.value} {Scope.FIRST_NAME_READ.value} {Scope.RELATIONSHIPS_READ.value} {Scope.RELATIONSHIPS_WRITE.value}",
            "X-Authenticated-Userid": profile_id,
            "X-Consumer-Username": "app_1"
        })
        self.assertEqual(200, response.status_code)
        json_response = json.loads(response.data)
        self.assertEqual(relationships, json_response)

        mock_patch.assert_called_once()
        self.service_collector_connector.hub_connector.get_app_details.assert_called_once()
        self.service_collector_connector.hub_connector.get_app_developers.assert_called_once()

    def test_put_oauth_no_read_permission(self):
        profile_id = "1"
        relationships = [
            {
                "appId": "4",
                "userId": "4c51ee0b-b7ec-4577-9b21-ae6832656e33",
                "type": "friend",
                "weight": 0.2
            }
        ]

        patched_profile = PatchWeNetUserProfile(profile_id=profile_id, relationships=relationships)

        mock_patch = Mock(return_value=patched_profile)
        self.service_collector_connector.profile_manager_collector.patch_user_profile = mock_patch
        self.service_collector_connector.hub_connector.get_app_details = Mock(return_value=self.app1)
        self.service_collector_connector.hub_connector.get_app_developers = Mock(return_value=self.developer_list)

        response = self.client.put(f"/user/profile/{profile_id}/relationships", json=relationships, headers={
            "apikey": self.AUTHORIZED_APIKEY,
            "x-wenet-source": WenetSource.OAUTH2_AUTHORIZATION_CODE.value,
            "X-Authenticated-Scope": f"{Scope.ID_READ.value} {Scope.FIRST_NAME_READ.value} {Scope.RELATIONSHIPS_WRITE.value}",
            "X-Authenticated-Userid": profile_id,
            "X-Consumer-Username": "app_1"
        })
        self.assertEqual(200, response.status_code)
        json_response = json.loads(response.data)
        self.assertEqual([], json_response)

        mock_patch.assert_called_once()
        self.service_collector_connector.hub_connector.get_app_details.assert_called_once()
        self.service_collector_connector.hub_connector.get_app_developers.assert_called_once()

    def test_put_oauth_no_permission(self):
        profile_id = "1"
        relationships = [
            {
                "appId": "4",
                "userId": "4c51ee0b-b7ec-4577-9b21-ae6832656e33",
                "type": "friend",
                "weight": 0.2
            }
        ]

        patched_profile = PatchWeNetUserProfile(profile_id=profile_id, relationships=relationships)

        mock_patch = Mock(return_value=patched_profile)
        self.service_collector_connector.profile_manager_collector.patch_user_profile = mock_patch
        self.service_collector_connector.hub_connector.get_app_details = Mock(return_value=self.app1)
        self.service_collector_connector.hub_connector.get_app_developers = Mock(return_value=self.developer_list)

        response = self.client.put(f"/user/profile/{profile_id}/relationships", json=relationships, headers={
            "apikey": self.AUTHORIZED_APIKEY,
            "x-wenet-source": WenetSource.OAUTH2_AUTHORIZATION_CODE.value,
            "X-Authenticated-Scope": f"{Scope.ID_READ.value} {Scope.FIRST_NAME_READ.value} {Scope.RELATIONSHIPS_READ.value}",
            "X-Authenticated-Userid": profile_id,
            "X-Consumer-Username": "app_1"
        })
        self.assertEqual(403, response.status_code)

        mock_patch.assert_not_called()
        self.service_collector_connector.hub_connector.get_app_details.assert_called_once()
        self.service_collector_connector.hub_connector.get_app_developers.assert_called_once()

    def test_put_oauth_2(self):
        profile_id = "1"
        relationships = [
            {
                "appId": "4",
                "userId": "4c51ee0b-b7ec-4577-9b21-ae6832656e33",
                "type": "friend",
                "weight": 0.2
            }
        ]

        mock_put = Mock(return_value=None)
        self.service_collector_connector.profile_manager_collector.update_user_profile = mock_put
        self.service_collector_connector.hub_connector.get_app_details = Mock(return_value=self.app1)
        self.service_collector_connector.hub_connector.get_app_developers = Mock(return_value=self.developer_list)

        response = self.client.put(f"/user/profile/2/relationships", json=relationships, headers={
            "apikey": self.AUTHORIZED_APIKEY,
            "x-wenet-source": WenetSource.OAUTH2_AUTHORIZATION_CODE.value,
            "X-Authenticated-Scope": f"{Scope.ID_READ.value} {Scope.FIRST_NAME_READ.value}",  # TODO add writing scope when will be added
            "X-Authenticated-Userid": profile_id,
            "X-Consumer-Username": "app_1"
        })
        self.assertEqual(401, response.status_code)

        mock_put.assert_not_called()
        self.service_collector_connector.hub_connector.get_app_details.assert_called_once()
        self.service_collector_connector.hub_connector.get_app_developers.assert_called_once()

    def test_put_not_authorized(self):
        profile_id = "profile_id"
        relationships = [
            {
                "appId": "4",
                "userId": "4c51ee0b-b7ec-4577-9b21-ae6832656e33",
                "type": "friend",
                "weight": 0.2
            }
        ]

        mock_put = Mock(return_value=None)
        self.service_collector_connector.profile_manager_collector.update_user_profile = mock_put

        response = self.client.put(f"/user/profile/{profile_id}/relationships", json=relationships)
        self.assertEqual(401, response.status_code)

        mock_put.assert_not_called()

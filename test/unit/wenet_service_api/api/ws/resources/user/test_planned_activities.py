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


class TestWeNetUserPlannedActivitiesInterface(CommonTestCase):

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
            planned_activities=[
                {
                    "id": "hfdsfs888",
                    "startTime": {},
                    "endTime": {},
                    "description": "A few beers for relaxing",
                    "attendees": [
                        "15d85f1d-b1ce-48de-b221-bec9ae954a88"
                    ],
                    "status": "confirmed"
                }
            ],
            relevant_locations=[],
            personal_behaviours=[],
            materials=[],
            competences=[],
            meanings=[]
        )

        mock_get = Mock(return_value=profile)
        self.service_collector_connector.profile_manager_collector.get_user_profile = mock_get

        response = self.client.get("/user/profile/profile-id/plannedActivities", headers={"apikey": self.AUTHORIZED_APIKEY, "x-wenet-source": WenetSource.COMPONENT.value})
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.data)
        self.assertEqual(profile.planned_activities, json_data)
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
            planned_activities=[
                {
                    "id": "hfdsfs888",
                    "startTime": {},
                    "endTime": {},
                    "description": "A few beers for relaxing",
                    "attendees": [
                        "15d85f1d-b1ce-48de-b221-bec9ae954a88"
                    ],
                    "status": "confirmed"
                }
            ],
            relevant_locations=[],
            personal_behaviours=[],
            materials=[],
            competences=[],
            meanings=[]
        )

        mock_get = Mock(return_value=deepcopy(profile))
        self.service_collector_connector.hub_connector.get_app_details = Mock(return_value=self.app)
        self.service_collector_connector.profile_manager_collector.get_user_profile = mock_get
        self.service_collector_connector.hub_connector.get_user_ids_for_app = Mock(return_value=self.user_list)

        response = self.client.get("/user/profile/1/plannedActivities", headers={
            "apikey": self.AUTHORIZED_APIKEY,
            "x-wenet-source": WenetSource.OAUTH2_AUTHORIZATION_CODE.value,
            "X-Authenticated-Scope": f"{Scope.ID_READ.value} {Scope.FIRST_NAME_READ.value} {Scope.ACTIVITIES_READ.value}",
            "X-Authenticated-Userid": profile_id,
            "X-Consumer-Username": "app_1"
        })
        self.assertEqual(200, response.status_code)
        json_data = json.loads(response.data)
        self.assertEqual(profile.planned_activities, json_data)

        mock_get.assert_called_once()
        self.service_collector_connector.hub_connector.get_app_details.assert_called_once()
        self.service_collector_connector.hub_connector.get_user_ids_for_app.assert_not_called()

    def test_get_oauth_missing_scope(self):
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
            planned_activities=[
                {
                    "id": "hfdsfs888",
                    "startTime": {},
                    "endTime": {},
                    "description": "A few beers for relaxing",
                    "attendees": [
                        "15d85f1d-b1ce-48de-b221-bec9ae954a88"
                    ],
                    "status": "confirmed"
                }
            ],
            relevant_locations=[],
            personal_behaviours=[],
            materials=[],
            competences=[],
            meanings=[]
        )

        mock_get = Mock(return_value=deepcopy(profile))
        self.service_collector_connector.hub_connector.get_app_details = Mock(return_value=self.app)
        self.service_collector_connector.profile_manager_collector.get_user_profile = mock_get
        self.service_collector_connector.hub_connector.get_user_ids_for_app = Mock(return_value=self.user_list)

        response = self.client.get("/user/profile/1/plannedActivities", headers={
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
            planned_activities=[
                {
                    "id": "hfdsfs888",
                    "startTime": {},
                    "endTime": {},
                    "description": "A few beers for relaxing",
                    "attendees": [
                        "15d85f1d-b1ce-48de-b221-bec9ae954a88"
                    ],
                    "status": "confirmed"
                }
            ],
            relevant_locations=[],
            personal_behaviours=[],
            materials=[],
            competences=[],
            meanings=[]
        )

        mock_get = Mock(return_value=deepcopy(profile))
        self.service_collector_connector.profile_manager_collector.get_user_profile = mock_get
        self.service_collector_connector.hub_connector.get_app_details = Mock(return_value=self.app1)
        self.service_collector_connector.hub_connector.get_app_developers = Mock(return_value=self.developer_list)

        response = self.client.get(f"/user/profile/{profile_id}/plannedActivities", headers={
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
        response = self.client.get("/user/profile/1/plannedActivities")
        self.assertEqual(response.status_code, 401)
        mock_get.assert_not_called()

    def test_put(self):
        profile_id = "1"
        planned_activities = [
            {
                "id": "hfdsfs888",
                "startTime": {},
                "endTime": {},
                "description": "A few beers for relaxing",
                "attendees": [
                    "15d85f1d-b1ce-48de-b221-bec9ae954a88"
                ],
                "status": "confirmed"
            }
        ]

        patched_profile = PatchWeNetUserProfile(profile_id=profile_id, planned_activities=planned_activities)

        mock_patch = Mock(return_value=patched_profile)
        self.service_collector_connector.profile_manager_collector.patch_user_profile = mock_patch

        response = self.client.put(f"/user/profile/{profile_id}/plannedActivities", json=planned_activities, headers={"apikey": self.AUTHORIZED_APIKEY, "x-wenet-source": WenetSource.COMPONENT.value})
        self.assertEqual(200, response.status_code)
        json_response = json.loads(response.data)
        self.assertEqual(planned_activities, json_response)
        mock_patch.assert_called_once()

    def test_put_oauth(self):
        profile_id = "1"
        planned_activities = [
            {
                "id": "hfdsfs888",
                "startTime": {},
                "endTime": {},
                "description": "A few beers for relaxing",
                "attendees": [
                    "15d85f1d-b1ce-48de-b221-bec9ae954a88"
                ],
                "status": "confirmed"
            }
        ]

        patched_profile = PatchWeNetUserProfile(profile_id=profile_id, planned_activities=planned_activities)

        mock_patch = Mock(return_value=patched_profile)
        self.service_collector_connector.profile_manager_collector.patch_user_profile = mock_patch
        self.service_collector_connector.hub_connector.get_app_details = Mock(return_value=self.app1)
        self.service_collector_connector.hub_connector.get_app_developers = Mock(return_value=self.developer_list)

        response = self.client.put(f"/user/profile/{profile_id}/plannedActivities", json=planned_activities, headers={
            "apikey": self.AUTHORIZED_APIKEY,
            "x-wenet-source": WenetSource.OAUTH2_AUTHORIZATION_CODE.value,
            "X-Authenticated-Scope": f"{Scope.ID_READ.value} {Scope.FIRST_NAME_READ.value} {Scope.ACTIVITIES_WRITE.value} {Scope.ACTIVITIES_READ.value}",
            "X-Authenticated-Userid": profile_id,
            "X-Consumer-Username": "app_1"
        })
        self.assertEqual(200, response.status_code)
        json_response = json.loads(response.data)
        self.assertEqual(planned_activities, json_response)

        mock_patch.assert_called_once()
        self.service_collector_connector.hub_connector.get_app_details.assert_called_once()
        self.service_collector_connector.hub_connector.get_app_developers.assert_called_once()

    def test_put_oauth_no_read_permission(self):
        profile_id = "1"
        planned_activities = [
            {
                "id": "hfdsfs888",
                "startTime": {},
                "endTime": {},
                "description": "A few beers for relaxing",
                "attendees": [
                    "15d85f1d-b1ce-48de-b221-bec9ae954a88"
                ],
                "status": "confirmed"
            }
        ]

        patched_profile = PatchWeNetUserProfile(profile_id=profile_id, planned_activities=planned_activities)

        mock_patch = Mock(return_value=patched_profile)
        self.service_collector_connector.profile_manager_collector.patch_user_profile = mock_patch
        self.service_collector_connector.hub_connector.get_app_details = Mock(return_value=self.app1)
        self.service_collector_connector.hub_connector.get_app_developers = Mock(return_value=self.developer_list)

        response = self.client.put(f"/user/profile/{profile_id}/plannedActivities", json=planned_activities,
                                   headers={
                                       "apikey": self.AUTHORIZED_APIKEY,
                                       "x-wenet-source": WenetSource.OAUTH2_AUTHORIZATION_CODE.value,
                                       "X-Authenticated-Scope": f"{Scope.ID_READ.value} {Scope.FIRST_NAME_READ.value} {Scope.ACTIVITIES_WRITE.value}",
                                       "X-Authenticated-Userid": profile_id,
                                       "X-Consumer-Username": "app_1"
                                   })
        self.assertEqual(200, response.status_code)
        json_response = json.loads(response.data)
        self.assertEqual([], json_response)

        mock_patch.assert_called_once()
        self.service_collector_connector.hub_connector.get_app_details.assert_called_once()
        self.service_collector_connector.hub_connector.get_app_developers.assert_called_once()

    def test_put_oauth_not_authorized(self):
        profile_id = "1"
        planned_activities = [
            {
                "id": "hfdsfs888",
                "startTime": {},
                "endTime": {},
                "description": "A few beers for relaxing",
                "attendees": [
                    "15d85f1d-b1ce-48de-b221-bec9ae954a88"
                ],
                "status": "confirmed"
            }
        ]

        patched_profile = PatchWeNetUserProfile(profile_id=profile_id, planned_activities=planned_activities)

        mock_patch = Mock(return_value=patched_profile)
        self.service_collector_connector.profile_manager_collector.patch_user_profile = mock_patch
        self.service_collector_connector.hub_connector.get_app_details = Mock(return_value=self.app1)
        self.service_collector_connector.hub_connector.get_app_developers = Mock(return_value=self.developer_list)

        response = self.client.put(f"/user/profile/{profile_id}/plannedActivities", json=planned_activities, headers={
            "apikey": self.AUTHORIZED_APIKEY,
            "x-wenet-source": WenetSource.OAUTH2_AUTHORIZATION_CODE.value,
            "X-Authenticated-Scope": f"{Scope.ID_READ.value} {Scope.FIRST_NAME_READ.value} {Scope.ACTIVITIES_READ.value}",
            "X-Authenticated-Userid": profile_id,
            "X-Consumer-Username": "app_1"
        })
        self.assertEqual(403, response.status_code)

        mock_patch.assert_not_called()
        self.service_collector_connector.hub_connector.get_app_details.assert_called_once()
        self.service_collector_connector.hub_connector.get_app_developers.assert_called_once()

    def test_put_oauth_2(self):
        profile_id = "1"
        planned_activities = [
            {
                "id": "hfdsfs888",
                "startTime": {},
                "endTime": {},
                "description": "A few beers for relaxing",
                "attendees": [
                    "15d85f1d-b1ce-48de-b221-bec9ae954a88"
                ],
                "status": "confirmed"
            }
        ]

        mock_put = Mock(return_value=None)
        self.service_collector_connector.profile_manager_collector.update_user_profile = mock_put
        self.service_collector_connector.hub_connector.get_app_details = Mock(return_value=self.app1)
        self.service_collector_connector.hub_connector.get_app_developers = Mock(return_value=self.developer_list)

        response = self.client.put(f"/user/profile/2/plannedActivities", json=planned_activities, headers={
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
        planned_activities = [
            {
                "id": "hfdsfs888",
                "startTime": {},
                "endTime": {},
                "description": "A few beers for relaxing",
                "attendees": [
                    "15d85f1d-b1ce-48de-b221-bec9ae954a88"
                ],
                "status": "confirmed"
            }
        ]

        mock_put = Mock(return_value=None)
        self.service_collector_connector.profile_manager_collector.update_user_profile = mock_put

        response = self.client.put(f"/user/profile/{profile_id}/plannedActivities", json=planned_activities)
        self.assertEqual(401, response.status_code)

        mock_put.assert_not_called()

from __future__ import absolute_import, annotations

import json
from datetime import datetime

from mock import Mock

from tests.wenet_service_api_test.api.common.common_test_case import CommonTestCase
from wenet.model.app import AppDTO, App, AppStatus
from wenet.model.user.profile import WeNetUserProfile
from wenet_service_api.api.ws.resource.common import WenetSource, Scope


class TestAuthentication(CommonTestCase):

    app = App(
        app_id="c0b7f45b-06c7-449c-9cc0-f778d7800193",
        status=AppStatus.STATUS_ACTIVE,
        message_callback_url="url",
        metadata={},
        creation_ts=int(datetime(2020, 2, 27).timestamp()),
        last_update_ts=int(datetime(2020, 2, 27).timestamp()),
        image_url="url",
        name="app_name",
        owner_id=1
    )

    app_inactive = App(
        app_id="c0b7f45b-06c7-449c-9cc0-f778d7800193",
        status=AppStatus.STATUS_NOT_ACTIVE,
        message_callback_url="url",
        metadata={},
        creation_ts=int(datetime(2020, 2, 27).timestamp()),
        last_update_ts=int(datetime(2020, 2, 27).timestamp()),
        image_url="url",
        name="app_name",
        owner_id=1
    )

    app_dto = AppDTO.from_app(app)

    user_list = ["1", "2", "3", "4"]
    developer_list = ["1", "2"]

    user_profile = WeNetUserProfile.empty(None)

    def setUp(self) -> None:
        super().setUp()

    def test_component_authentication(self):
        app_id = self.app.app_id

        self.service_collector_connector.hub_connector.get_app_details = Mock(return_value=self.app)
        response = self.client.get(f"/app/{app_id}", headers={"apikey": self.AUTHORIZED_APIKEY,  "x-wenet-source": WenetSource.COMPONENT.value})

        self.assertEqual(response.status_code, 200)

        json_data = json.loads(response.data)
        result_app = AppDTO.from_repr(json_data)

        self.assertIsInstance(result_app, AppDTO)
        self.assertEqual(app_id, result_app.app_id)
        self.assertEqual(self.app_dto, result_app)

    def test_component_authentication2(self):
        app_id = self.app.app_id

        response = self.client.get(f"/app/{app_id}", headers={"apikey": "asd",  "x-wenet-source": WenetSource.COMPONENT.value})

        self.assertEqual(response.status_code, 401)

    def test_component_authentication3(self):
        app_id = self.app.app_id

        response = self.client.get(f"/app/{app_id}", headers={"apikey": self.AUTHORIZED_APIKEY})

        self.assertEqual(response.status_code, 401)

    def test_wrong_header(self):
        app_id = self.app.app_id

        response = self.client.get(f"/app/{app_id}", headers={"x-wenet-source": "asd"})

        self.assertEqual(response.status_code, 401)

    def test_oauth(self):

        self.service_collector_connector.hub_connector.get_app_details = Mock(return_value=self.app)
        self.service_collector_connector.profile_manager_collector.get_user_profile = Mock(return_value=self.user_profile)
        self.service_collector_connector.hub_connector.get_user_ids_for_app = Mock(return_value=self.user_list)

        response = self.client.get(f"/user/profile/1", headers={
            "x-wenet-source": WenetSource.OAUTH2_AUTHORIZATION_CODE.value,
            "X-Authenticated-Userid": "1",
            "X-Authenticated-Scope": f"{Scope.ID.value} {Scope.NATIONALITY.value} {Scope.PHONE_NUMBER.value}",
            "X-Consumer-Username": f"app_{self.app.app_id}",
            "apikey": self.AUTHORIZED_APIKEY
        })

        self.assertEqual(response.status_code, 200)
        self.service_collector_connector.hub_connector.get_user_ids_for_app.assert_called_once()
        self.service_collector_connector.hub_connector.get_app_details.assert_called_once()
        self.service_collector_connector.profile_manager_collector.get_user_profile.assert_called_once()

    def test_oauth_development(self):

        self.service_collector_connector.hub_connector.get_app_details = Mock(return_value=self.app_inactive)
        self.service_collector_connector.profile_manager_collector.get_profile = Mock(return_value=self.user_profile)
        self.service_collector_connector.hub_connector.get_app_developers = Mock(return_value=self.developer_list)

        response = self.client.get(f"/user/profile/4", headers={
            "x-wenet-source": WenetSource.OAUTH2_AUTHORIZATION_CODE.value,
            "X-Authenticated-Userid": "4",
            "X-Authenticated-Scope": f"{Scope.ID.value} {Scope.NATIONALITY.value} {Scope.PHONE_NUMBER.value}",
            "X-Consumer-Username": f"app_{self.app.app_id}",
            "apikey": self.AUTHORIZED_APIKEY
        })

        self.assertEqual(response.status_code, 403)

    def test_oauth_development_developer(self):

        self.service_collector_connector.hub_connector.get_app_details = Mock(return_value=self.app_inactive)
        self.service_collector_connector.profile_manager_collector.get_user_profile = Mock(return_value=self.user_profile)
        self.service_collector_connector.hub_connector.get_app_developers = Mock(return_value=self.developer_list)
        self.service_collector_connector.hub_connector.get_user_ids_for_app = Mock(return_value=self.user_list)

        response = self.client.get(f"/user/profile/2", headers={
            "x-wenet-source": WenetSource.OAUTH2_AUTHORIZATION_CODE.value,
            "X-Authenticated-Userid": "2",
            "X-Authenticated-Scope": f"{Scope.ID.value} {Scope.NATIONALITY.value} {Scope.PHONE_NUMBER.value}",
            "X-Consumer-Username": f"app_{self.app.app_id}",
            "apikey": self.AUTHORIZED_APIKEY
        })

        self.assertEqual(response.status_code, 200)
        self.service_collector_connector.hub_connector.get_app_details.assert_called_once()
        self.service_collector_connector.profile_manager_collector.get_user_profile.assert_called_once()
        self.service_collector_connector.hub_connector.get_app_developers.assert_called_once()
        self.service_collector_connector.hub_connector.get_user_ids_for_app.assert_called_once()


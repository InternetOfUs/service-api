from __future__ import absolute_import, annotations

import json
from datetime import datetime

from mock import Mock

from wenet.model.app import AppDTO, App, AppStatus

from test.unit.wenet_service_api.api.common.common_test_case import CommonTestCase
from wenet_service_api.api.ws.resource.common import WenetSource
from wenet_service_api.common.exception.exceptions import ResourceNotFound


class TestAppResourceInterface(CommonTestCase):

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

    app_dto = AppDTO.from_app(app)

    def setUp(self) -> None:
        super().setUp()

    def test_get(self):

        app_id = self.app.app_id

        self.service_collector_connector.hub_connector.get_app_details = Mock(return_value=self.app)

        response = self.client.get(f"/app/{app_id}", headers={"apikey": self.AUTHORIZED_APIKEY, "x-wenet-source": WenetSource.COMPONENT.value})

        self.assertEqual(response.status_code, 200)

        json_data = json.loads(response.data)
        result_app = AppDTO.from_repr(json_data)

        self.assertIsInstance(result_app, AppDTO)
        self.assertEqual(app_id, result_app.app_id)
        self.assertEqual(self.app_dto, result_app)

        self.service_collector_connector.hub_connector.get_app_details.assert_called_once()

    def test_get_not_authorized(self):

        app_id = self.app.app_id

        response = self.client.get(f"/app/{app_id}")

        self.assertEqual(response.status_code, 401)

    def test_get2(self):

        app_id = "5354f062-ace2-4da9-bee8-b2d286814636"

        self.service_collector_connector.hub_connector.get_app_details = Mock(side_effect=ResourceNotFound)

        response = self.client.get(f"/app/{app_id}", headers={"apikey": self.AUTHORIZED_APIKEY, "x-wenet-source": WenetSource.COMPONENT.value})

        self.assertEqual(response.status_code, 404)


class TestListAppUserInterface(CommonTestCase):
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

    app_dto = AppDTO.from_app(app)

    def setUp(self) -> None:
        super().setUp()

    def test_get(self):

        app_id = self.app.app_id

        user_list = ["1", "2", "3", "4"]

        mock_get = Mock(return_value=user_list)

        self.service_collector_connector.hub_connector.get_app_details = Mock(return_value=self.app)
        self.service_collector_connector.hub_connector.get_user_ids_for_app = mock_get

        response = self.client.get(f"/app/{app_id}/users", headers={"apikey": self.AUTHORIZED_APIKEY, "x-wenet-source": WenetSource.COMPONENT.value})

        self.assertEqual(response.status_code, 200)

        json_data = json.loads(response.data)
        self.assertIsInstance(json_data, list)

        self.assertEqual(user_list, json_data)

        mock_get.assert_called_once()
        self.service_collector_connector.hub_connector.get_app_details.assert_called_once()

    def test_get_not_authorized(self):

        app_id = self.app.app_id

        response = self.client.get(f"/app/{app_id}/users")

        self.assertEqual(response.status_code, 401)

    def test_get2(self):

        app_id = "5354f062-ace2-4da9-bee8-b2d286814636"

        self.service_collector_connector.hub_connector.get_app_details = Mock(side_effect=ResourceNotFound)

        response = self.client.get(f"/app/{app_id}/users", headers={"apikey": self.AUTHORIZED_APIKEY, "x-wenet-source": WenetSource.COMPONENT.value})

        self.assertEqual(response.status_code, 404)
        self.service_collector_connector.hub_connector.get_app_details.assert_called_once()

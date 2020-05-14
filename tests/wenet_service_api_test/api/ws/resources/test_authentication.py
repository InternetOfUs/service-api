from __future__ import absolute_import, annotations

import json
from datetime import datetime

from tests.wenet_service_api_test.api.common.common_test_case import CommonTestCase
from wenet.common.model.app.app_dto import AppDTO
from wenet_service_api.api.ws.resource.common import WenetSources
from wenet_service_api.model.app import App


class TestAuthentication(CommonTestCase):

    app = App(
        app_id="c0b7f45b-06c7-449c-9cc0-f778d7800193",
        status="1",
        name="name",
        description="description",
        app_token="dshfgsahjfsdfdsjhfgsd",
        message_callback_url="url",
        metadata={},
        creation_ts=int(datetime(2020, 2, 27).timestamp()),
        last_update_ts=int(datetime(2020, 2, 27).timestamp())
    )

    app_dto = app.to_app_dto()

    def setUp(self) -> None:
        super().setUp()
        self.dao_collector.app_dao.create_or_update(self.app)

    def test_component_authentication(self):
        app_id = self.app.app_id

        response = self.client.get(f"/app/{app_id}", headers={"apikey": self.AUTHORIZED_APIKEY,  "x-wenet-source": WenetSources.COMPONENT.value})

        self.assertEqual(response.status_code, 200)

        json_data = json.loads(response.data)
        result_app = AppDTO.from_repr(json_data)

        self.assertIsInstance(result_app, AppDTO)
        self.assertEqual(app_id, result_app.app_id)
        self.assertEqual(self.app_dto, result_app)

    def test_component_authentication2(self):
        app_id = self.app.app_id

        response = self.client.get(f"/app/{app_id}", headers={"apikey": "asd",  "x-wenet-source": WenetSources.COMPONENT.value})

        self.assertEqual(response.status_code, 401)

    def test_component_authentication3(self):
        app_id = self.app.app_id

        response = self.client.get(f"/app/{app_id}", headers={"apikey": self.AUTHORIZED_APIKEY})

        self.assertEqual(response.status_code, 401)

    def test_wrong_header(self):
        app_id = self.app.app_id

        response = self.client.get(f"/app/{app_id}", headers={"x-wenet-source": "asd"})

        self.assertEqual(response.status_code, 401)

    def test_app_authentication(self):
        app_id = self.app.app_id

        response = self.client.get(
            f"/app/{app_id}",
            headers={
                "apikey": self.AUTHORIZED_APIKEY,
                "x-wenet-source": WenetSources.APP.value,
                "appId": self.app.app_id,
                "appToken": self.app.app_token
            }
        )

        self.assertEqual(response.status_code, 200)

        json_data = json.loads(response.data)
        result_app = AppDTO.from_repr(json_data)

        self.assertIsInstance(result_app, AppDTO)
        self.assertEqual(app_id, result_app.app_id)
        self.assertEqual(self.app_dto, result_app)

    def test_app_authentication2(self):
        app_id = self.app.app_id

        response = self.client.get(
            f"/app/{app_id}",
            headers={
                "apikey": self.AUTHORIZED_APIKEY,
                "x-wenet-source": WenetSources.APP.value,
                "appId": "asd",
                "appToken": self.app.app_token
            }
        )

        self.assertEqual(response.status_code, 401)

    def test_app_authentication3(self):
        app_id = self.app.app_id

        response = self.client.get(
            f"/app/{app_id}",
            headers={
                "apikey": self.AUTHORIZED_APIKEY,
                "x-wenet-source": WenetSources.APP.value,
                "appId": self.app.app_id,
                "appToken": "asd"
            }
        )

        self.assertEqual(response.status_code, 401)

    def test_app_authentication4(self):
        app_id = self.app.app_id

        response = self.client.get(
            f"/app/{app_id}",
            headers={
                "apikey": self.AUTHORIZED_APIKEY,
                "appId": self.app.app_id,
                "appToken": self.app.app_token
            }
        )

        self.assertEqual(response.status_code, 401)


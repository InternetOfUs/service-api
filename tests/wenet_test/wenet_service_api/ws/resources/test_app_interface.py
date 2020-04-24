from __future__ import absolute_import, annotations

import json
from datetime import datetime

from tests.wenet_test.wenet_service_api.common.common_test_case import CommonTestCase
from wenet_service_api.model.app import App, AppDTO


# class TestAppPostInterface(CommonTestCase):
#
#     def test_post(self):
#
#         response = self.client.post("/app", json={"name": "app_name"}, headers={"apikey": self.AUTHORIZED_APIKEY})
#
#         self.assertEqual(response.status_code, 201)
#
#         json_data = json.loads(response.data)
#
#         app = App.from_repr(json_data)
#
#         self.assertIsInstance(app, App)
#         self.assertEqual("app_name", app.name)
#
#     def test_post_not_authorized(self):
#
#         response = self.client.post("/app", json={"name": "app_name"}, headers={"apikey": self.AUTHORIZED_APIKEY + "1"})
#
#         self.assertEqual(response.status_code, 403)
#
#     def test_post_not_authorized2(self):
#
#         response = self.client.post("/app", json={"name": "app_name"})
#
#         self.assertEqual(response.status_code, 403)


class TestAppResourceInterface(CommonTestCase):

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

    app_dto = AppDTO.from_app(app)

    def setUp(self) -> None:
        super().setUp()
        self.dao_collector.app_dao.create_or_update(self.app)

    def test_get(self):

        app_id = self.app.app_id

        response = self.client.get(f"/app/{app_id}", headers={"apikey": self.AUTHORIZED_APIKEY})

        self.assertEqual(response.status_code, 200)

        json_data = json.loads(response.data)
        result_app = AppDTO.from_repr(json_data)

        self.assertIsInstance(result_app, AppDTO)
        self.assertEqual(app_id, result_app.app_id)
        self.assertEqual(self.app_dto, result_app)

    def test_get_not_authorized(self):

        app_id = self.app.app_id

        response = self.client.get(f"/app/{app_id}")

        self.assertEqual(response.status_code, 403)

    def test_get2(self):

        app_id = "5354f062-ace2-4da9-bee8-b2d286814636"

        response = self.client.get(f"/app/{app_id}", headers={"apikey": self.AUTHORIZED_APIKEY})

        self.assertEqual(response.status_code, 404)

    # def test_put(self):
    #     app_id = self.app.app_id
    #     app_name = "updated app name"
    #     app_token = "XkLOHcHbtDEGusT982Ji-gd1qBp9U_WiPXWI7XMGwfM"
    #     app_repr = {
    #         "appId": "asd",
    #         "appToken": app_token,
    #         "name": app_name
    #     }
    #
    #     response = self.client.put(f"/app/{app_id}", json=app_repr, headers={"apikey": self.AUTHORIZED_APIKEY})
    #
    #     self.assertEqual(response.status_code, 200)
    #
    #     json_data = json.loads(response.data)
    #     app = App.from_repr(json_data)
    #
    #     self.assertIsInstance(app, App)
    #     self.assertEqual(app_id, app.app_id)
    #     self.assertEqual(app_name, app.name)
    #     self.assertEqual(app_token, app.app_token)

    # def test_put_not_authorized(self):
    #     app_id = self.app.app_id
    #     app_name = "updated app name"
    #     app_token = "XkLOHcHbtDEGusT982Ji-gd1qBp9U_WiPXWI7XMGwfM"
    #     app_repr = {
    #         "appId": "asd",
    #         "appToken": app_token,
    #         "name": app_name
    #     }
    #
    #     response = self.client.put(f"/app/{app_id}", json=app_repr)
    #
    #     self.assertEqual(response.status_code, 403)
    #
    # def test_put2(self):
    #     app_id = "5354f062-ace2-4da9-bee8-b2d286814636"
    #     app_name = "updated app name"
    #     app_token = "XkLOHcHbtDEGusT982Ji-gd1qBp9U_WiPXWI7XMGwfM"
    #     app_repr = {
    #         "appId": "asd",
    #         "appToken": app_token,
    #         "name": app_name
    #     }
    #
    #     response = self.client.put(f"/app/{app_id}", json=app_repr, headers={"apikey": self.AUTHORIZED_APIKEY})
    #
    #     self.assertEqual(response.status_code, 404)

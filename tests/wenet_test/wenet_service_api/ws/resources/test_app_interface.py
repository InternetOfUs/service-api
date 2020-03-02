from __future__ import absolute_import, annotations

import json
from datetime import datetime

from tests.wenet_test.wenet_service_api.common.common_test_case import CommonTestCase
from wenet.model.app import App


class TestAppPostInterface(CommonTestCase):

    def test_post(self):

        response = self.client.post("/app", json={"name": "app_name"})

        self.assertEqual(response.status_code, 201)

        json_data = json.loads(response.data)

        app = App.from_repr(json_data)

        self.assertIsInstance(app, App)
        self.assertEqual("app_name", app.name)


class TestAppResourceInterface(CommonTestCase):

    app = App(
        app_id="c0b7f45b-06c7-449c-9cc0-f778d7800193",
        app_token="dshfgsahjfsdfdsjhfgsd",
        name="app name",
        creation_ts=datetime(2020, 2, 27),
        last_update_ts=datetime(2020, 2, 27)
    )

    def setUp(self) -> None:
        super().setUp()
        self.dao_collector.app_dao.create_or_update(self.app)

    def test_get(self):

        app_id = self.app.app_id

        response = self.client.get(f"/app/{app_id}")

        self.assertEqual(response.status_code, 200)

        json_data = json.loads(response.data)
        app = App.from_repr(json_data)

        self.assertIsInstance(app, App)
        self.assertEqual(app_id, app.app_id)
        self.assertEqual(self.app, app)

    def test_get2(self):

        app_id = "5354f062-ace2-4da9-bee8-b2d286814636"

        response = self.client.get(f"/app/{app_id}")

        self.assertEqual(response.status_code, 404)

    def test_put(self):
        app_id = self.app.app_id
        app_name = "updated app name"
        app_token = "XkLOHcHbtDEGusT982Ji-gd1qBp9U_WiPXWI7XMGwfM"
        app_repr = {
            "appId": "asd",
            "appToken": app_token,
            "name": app_name
        }

        response = self.client.put(f"/app/{app_id}", json=app_repr)

        self.assertEqual(response.status_code, 200)

        json_data = json.loads(response.data)
        app = App.from_repr(json_data)

        self.assertIsInstance(app, App)
        self.assertEqual(app_id, app.app_id)
        self.assertEqual(app_name, app.name)
        self.assertEqual(app_token, app.app_token)

    def test_put2(self):
        app_id = "5354f062-ace2-4da9-bee8-b2d286814636"
        app_name = "updated app name"
        app_token = "XkLOHcHbtDEGusT982Ji-gd1qBp9U_WiPXWI7XMGwfM"
        app_repr = {
            "appId": "asd",
            "appToken": app_token,
            "name": app_name
        }

        response = self.client.put(f"/app/{app_id}", json=app_repr)

        self.assertEqual(response.status_code, 404)
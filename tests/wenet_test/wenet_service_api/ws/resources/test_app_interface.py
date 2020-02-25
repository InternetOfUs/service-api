from __future__ import absolute_import, annotations

import json

from tests.wenet_test.wenet_service_api.common.common_test_case import CommonTestCase
from wenet.model.App import App


class TestAppPostInterface(CommonTestCase):

    def test_post(self):

        response = self.client.post("/app", json={"name": "app_name"})

        self.assertEqual(response.status_code, 201)

        json_data = json.loads(response.data)

        app = App.from_repr(json_data)

        self.assertIsInstance(app, App)
        self.assertEqual("app_name", app.name)


class TestAppResourceInterface(CommonTestCase):

    def test_get(self):

        app_id = "c0b7f45b-06c7-449c-9cc0-f778d7800193"

        response = self.client.get(f"/app/{app_id}")

        self.assertEqual(response.status_code, 200)

        json_data = json.loads(response.data)
        app = App.from_repr(json_data)

        self.assertIsInstance(app, App)
        self.assertEqual(app_id, app.app_id)

    def test_put(self):
        app_id = "c0b7f45b-06c7-449c-9cc0-f778d7800193"
        app_name = "app_name"
        app_repr = {
            "appId": "asd",
            "appToken": "XkLOHcHbtDEGusT982Ji-gd1qBp9U_WiPXWI7XMGwfM",
            "name": app_name
        }

        response = self.client.put(f"/app/{app_id}", json=app_repr)

        self.assertEqual(response.status_code, 200)

        json_data = json.loads(response.data)
        app = App.from_repr(json_data)

        self.assertIsInstance(app, App)
        self.assertEqual(app_id, app.app_id)
        self.assertEqual(app_name, app.name)

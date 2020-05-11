from __future__ import absolute_import, annotations

import json
from datetime import datetime

from tests.wenet_service_api_test.api.common.common_test_case import CommonTestCase
from wenet.common.model.app.app_dto import AppDTO
from wenet_service_api.model.app import App, UserAccountTelegram


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

    app_dto = app.to_app_dto()

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


class TestListAppUserInterface(CommonTestCase):
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

    user1 = UserAccountTelegram(
        user_account_id=1,
        app_id="c0b7f45b-06c7-449c-9cc0-f778d7800193",
        user_id=1,
        telegram_id=1,
        creation_ts=11,
        last_update_ts=11,
        metadata=None,
        active=1
    )

    user2 = UserAccountTelegram(
        user_account_id=2,
        app_id="c0b7f45b-06c7-449c-9cc0-f778d7800193",
        user_id=2,
        telegram_id=1,
        creation_ts=11,
        last_update_ts=11,
        metadata=None,
        active=1
    )

    user3 = UserAccountTelegram(
        user_account_id=3,
        app_id="c0b7f45b-06c7-449c-9cc0-f778d7800193",
        user_id=3,
        telegram_id=1,
        creation_ts=11,
        last_update_ts=11,
        metadata=None,
        active=0
    )

    user4 = UserAccountTelegram(
        user_account_id=4,
        app_id="c0b7f45b-06c7-449c-9cc0-f778d7800192",
        user_id=4,
        telegram_id=1,
        creation_ts=11,
        last_update_ts=11,
        metadata=None,
        active=1
    )

    app_dto = app.to_app_dto()

    def setUp(self) -> None:
        super().setUp()
        self.dao_collector.app_dao.create_or_update(self.app)
        self.dao_collector.user_account_telegram_dao.create_or_update(self.user1)
        self.dao_collector.user_account_telegram_dao.create_or_update(self.user2)
        self.dao_collector.user_account_telegram_dao.create_or_update(self.user3)
        self.dao_collector.user_account_telegram_dao.create_or_update(self.user4)

    def test_get(self):

        app_id = self.app.app_id

        response = self.client.get(f"/app/{app_id}/users", headers={"apikey": self.AUTHORIZED_APIKEY})

        self.assertEqual(response.status_code, 200)

        json_data = json.loads(response.data)
        self.assertIsInstance(json_data, list)

        id_set = set(x for x in json_data)

        self.assertEqual(len(id_set), len(json_data))
        self.assertEqual({"1", "2"}, id_set)

    def test_get_not_authorized(self):

        app_id = self.app.app_id

        response = self.client.get(f"/app/{app_id}/users")

        self.assertEqual(response.status_code, 403)

    def test_get2(self):

        app_id = "5354f062-ace2-4da9-bee8-b2d286814636"

        response = self.client.get(f"/app/{app_id}/users", headers={"apikey": self.AUTHORIZED_APIKEY})

        self.assertEqual(response.status_code, 404)

from __future__ import absolute_import, annotations

from datetime import datetime

from tests.wenet_test.wenet_service_api.common.common_test_case import CommonTestCase
from wenet.model.app import App, UserAccountTelegram
from wenet.model.authentication_account import TelegramAuthenticationAccount


class TestUserAuthenticateInterface(CommonTestCase):

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

    user_account_telegram = UserAccountTelegram(
        user_account_id=1,
        app_id="c0b7f45b-06c7-449c-9cc0-f778d7800193",
        user_id="user_id",
        telegram_id=11,
        creation_ts=1,
        last_update_ts=1,
        metadata={
            "key1": "value1"
        },
        active=1
    )

    def setUp(self) -> None:
        super().setUp()
        self.dao_collector.app_dao.create_or_update(self.app)
        self.dao_collector.user_account_telegram_dao.create_or_update(self.user_account_telegram)

    def test_get(self):

        telegram_user_account = TelegramAuthenticationAccount(
            app_id="c0b7f45b-06c7-449c-9cc0-f778d7800193",
            metadata={},
            telegram_id=11
        )

        response = self.client.post(f"/user/authenticate", headers={"apikey": self.AUTHORIZED_APIKEY}, json=telegram_user_account.to_repr())

        self.assertEqual(response.status_code, 200)

        json_data = response.json

        self.assertEqual(json_data["userId"], self.user_account_telegram.user_id)

    def test_get2(self):

        telegram_user_account = TelegramAuthenticationAccount(
            app_id="c0b7f45b-06c7-449c-9cc0-f778d7800193-wrong",
            metadata={},
            telegram_id=11
        )

        response = self.client.post(f"/user/authenticate", headers={"apikey": self.AUTHORIZED_APIKEY}, json=telegram_user_account.to_repr())

        self.assertEqual(response.status_code, 401)

    def test_get3(self):

        telegram_user_account = TelegramAuthenticationAccount(
            app_id="c0b7f45b-06c7-449c-9cc0-f778d7800193",
            metadata={},
            telegram_id=12
        )

        response = self.client.post(f"/user/authenticate", headers={"apikey": self.AUTHORIZED_APIKEY}, json=telegram_user_account.to_repr())

        self.assertEqual(response.status_code, 401)



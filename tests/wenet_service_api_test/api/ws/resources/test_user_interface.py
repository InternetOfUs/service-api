from __future__ import absolute_import, annotations

from datetime import datetime

from mock import Mock

from tests.wenet_service_api_test.api.common.common_test_case import CommonTestCase
from wenet_service_api.model.app import App, UserAccountTelegram
from wenet_service_api.model.authentication_account import TelegramAuthenticationAccount, WeNetUserWithAccounts


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
        user_id=1,
        telegram_id=11,
        creation_ts=1,
        last_update_ts=1,
        metadata={
            "key1": "value1"
        },
        active=1
    )

    user_account_telegram_inactive = UserAccountTelegram(
        user_account_id=2,
        app_id="c0b7f45b-06c7-449c-9cc0-f778d7800193",
        user_id=1,
        telegram_id=12,
        creation_ts=1,
        last_update_ts=1,
        metadata={
            "key1": "value1"
        },
        active=0
    )

    def setUp(self) -> None:
        super().setUp()
        self.dao_collector.app_dao.create_or_update(self.app)
        self.dao_collector.user_account_telegram_dao.create_or_update(self.user_account_telegram)
        self.dao_collector.user_account_telegram_dao.create_or_update(self.user_account_telegram_inactive)

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

    def test_get4(self):

        telegram_user_account = TelegramAuthenticationAccount(
            app_id="c0b7f45b-06c7-449c-9cc0-f778d7800193",
            metadata={},
            telegram_id=11
        )

        response = self.client.post(f"/user/authenticate", json=telegram_user_account.to_repr())

        self.assertEqual(response.status_code, 403)

    def test_get5(self):

        telegram_user_account = TelegramAuthenticationAccount(
            app_id="c0b7f45b-06c7-449c-9cc0-f778d7800193",
            metadata={},
            telegram_id=11
        )

        response = self.client.post(f"/user/authenticate", headers={"apikey": "asd"}, json=telegram_user_account.to_repr())

        self.assertEqual(response.status_code, 403)

    def test_get_inactive(self):

        telegram_user_account = TelegramAuthenticationAccount(
            app_id="c0b7f45b-06c7-449c-9cc0-f778d7800193",
            metadata={},
            telegram_id=12
        )

        response = self.client.post(f"/user/authenticate", headers={"apikey": self.AUTHORIZED_APIKEY}, json=telegram_user_account.to_repr())

        self.assertEqual(response.status_code, 401)


class TestUserMetadataInterface(CommonTestCase):
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
        user_id=1,
        telegram_id=11,
        creation_ts=1,
        last_update_ts=1,
        metadata={
            "key1": "value1"
        },
        active=1
    )

    user_account_telegram_inactive = UserAccountTelegram(
        user_account_id=2,
        app_id="c0b7f45b-06c7-449c-9cc0-f778d7800193",
        user_id=1,
        telegram_id=12,
        creation_ts=1,
        last_update_ts=1,
        metadata={
            "key1": "value1"
        },
        active=0
    )

    def setUp(self) -> None:
        super().setUp()
        self.dao_collector.app_dao.create_or_update(self.app)
        self.dao_collector.user_account_telegram_dao.create_or_update(self.user_account_telegram)
        self.dao_collector.user_account_telegram_dao.create_or_update(self.user_account_telegram_inactive)

    def test_post(self):
        telegram_user_account = TelegramAuthenticationAccount(
            app_id="c0b7f45b-06c7-449c-9cc0-f778d7800193",
            metadata={
                "key1": "value1"
            },
            telegram_id=11
        )

        response = self.client.post(f"/user/account/metadata", headers={"apikey": self.AUTHORIZED_APIKEY},
                                    json=telegram_user_account.to_repr())

        self.assertEqual(response.status_code, 200)

        updated_user_account = self.dao_collector.user_account_telegram_dao.get(telegram_user_account.app_id, telegram_user_account.telegram_id)
        self.assertEqual(updated_user_account.metadata, telegram_user_account.metadata)

    def test_post_invalid(self):
        telegram_user_account = TelegramAuthenticationAccount(
            app_id="c0b7f45b-06c7-449c-9cc0-f778d7800193",
            metadata={
                "key1": "value1"
            },
            telegram_id=12
        )
        mock_update = Mock()

        self.dao_collector.user_account_telegram_dao.create_or_update = mock_update

        response = self.client.post(f"/user/account/metadata", headers={"apikey": self.AUTHORIZED_APIKEY},
                                    json=telegram_user_account.to_repr())

        self.assertEqual(response.status_code, 401)
        mock_update.assert_not_called()

    def test_post_invalid2(self):
        telegram_user_account = TelegramAuthenticationAccount(
            app_id="c0b7f45b-06c7-449c-9cc0-f778d7800193",
            metadata={
                "key1": "value1"
            },
            telegram_id=11
        )
        mock_update = Mock()

        self.dao_collector.user_account_telegram_dao.create_or_update = mock_update

        response = self.client.post(f"/user/account/metadata", headers={"apikey": "asd"}, json=telegram_user_account.to_repr())

        self.assertEqual(response.status_code, 403)
        mock_update.assert_not_called()

    def test_post_invalid3(self):
        telegram_user_account = TelegramAuthenticationAccount(
            app_id="c0b7f45b-06c7-449c-9cc0-f778d7800193",
            metadata={
                "key1": "value1"
            },
            telegram_id=11
        )
        mock_update = Mock()

        self.dao_collector.user_account_telegram_dao.create_or_update = mock_update

        response = self.client.post(f"/user/account/metadata", json=telegram_user_account.to_repr())

        self.assertEqual(response.status_code, 403)
        mock_update.assert_not_called()


class TestUserAccountsInterface(CommonTestCase):
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
        user_id=1,
        telegram_id=11,
        creation_ts=1,
        last_update_ts=1,
        metadata={
            "key1": "value1"
        },
        active=1
    )

    user_account_telegram2 = UserAccountTelegram(
        user_account_id=2,
        app_id="c0b7f45b-06c7-449c-9cc0-f778d7800193",
        user_id=2,
        telegram_id=12,
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
        self.dao_collector.user_account_telegram_dao.create_or_update(self.user_account_telegram2)

    def test_get(self):
        response = self.client.get(f"/user/accounts?appId=c0b7f45b-06c7-449c-9cc0-f778d7800193&userId=1", headers={"apikey": self.AUTHORIZED_APIKEY})

        self.assertEqual(response.status_code, 200)

        json_data = response.json
        accounts = WeNetUserWithAccounts.from_repr(json_data)

        self.assertIsInstance(accounts, WeNetUserWithAccounts)
        self.assertEqual(1, len(accounts.accounts))
        self.assertEqual(1, accounts.accounts[0].user_id)

    def test_get2(self):
        response = self.client.get(f"/user/accounts?appId=c0b7f45b-06c7-449c-9cc0-f778d7800193&userId=1", headers={"apikey": "asd"})

        self.assertEqual(response.status_code, 403)

    def test_get3(self):
        response = self.client.get(f"/user/accounts?appId=c0b7f45b-06c7-449c-9cc0-f778d7800193&userId=1")

        self.assertEqual(response.status_code, 403)

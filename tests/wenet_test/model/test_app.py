from __future__ import absolute_import, annotations

from datetime import datetime
from unittest import TestCase

from wenet.model.app import App, AppDTO
from wenet.model.platform_dto import TelegramPlatformDTO


class TestAppDTO(TestCase):

    def test_repr(self):
        app = AppDTO(
            app_id="app id",
            app_token="token",
            creation_ts=datetime.utcfromtimestamp(1231231.0),
            last_update_ts=datetime.utcfromtimestamp(1231231.0),
            allowed_platforms=[
                TelegramPlatformDTO(
                    bot_id="bot_id"
                )
            ],
            message_callback_url="callback",
            metadata={}
        )

        from_repr = AppDTO.from_repr(app.to_repr())

        self.assertIsInstance(from_repr, AppDTO)
        self.assertEqual(app, from_repr)

    def test_repr2(self):
        app = AppDTO(
            app_id="app id",
            app_token="token",
            creation_ts=None,
            last_update_ts=None,
            allowed_platforms=[],
            message_callback_url="callback",
            metadata=None
        )

        from_repr = AppDTO.from_repr(app.to_repr())

        self.assertIsInstance(from_repr, AppDTO)
        self.assertEqual(app, from_repr)


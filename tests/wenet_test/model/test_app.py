from __future__ import absolute_import, annotations

from datetime import datetime
from unittest import TestCase

from wenet.model.App import App


class TestApp(TestCase):

    def test_repr(self):
        app = App(
            app_id="app id",
            app_token="token",
            name="name",
            creation_ts=datetime.utcfromtimestamp(1231231.0),
            last_update_ts=datetime.utcfromtimestamp(1231231.0)
        )

        from_repr = App.from_repr(app.to_repr())

        self.assertIsInstance(from_repr, App)
        self.assertEqual(app, from_repr)

    def test_repr2(self):
        app = App(
            app_id="app id",
            app_token="token",
            name="name",
            creation_ts=None,
            last_update_ts=None
        )

        from_repr = App.from_repr(app.to_repr())

        self.assertIsInstance(from_repr, App)
        self.assertEqual(app, from_repr)

from __future__ import absolute_import, annotations

from unittest import TestCase

from wenet.wenet_service_api.ws.ws import WsInterface


class CommonTestCase(TestCase):

    def setUp(self) -> None:
        super().setUp()
        api = WsInterface()
        api.get_application().testing = True
        self.client = api.get_application().test_client()

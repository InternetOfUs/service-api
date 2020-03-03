from __future__ import absolute_import, annotations

from unittest import TestCase

from tests.wenet_test.wenet_service_api.common.mocks import MockDaoCollector
from wenet.wenet_service_api.ws.ws import WsInterface


class CommonTestCase(TestCase):

    AUTHORIZED_APIKEY = "1234"

    def setUp(self) -> None:
        super().setUp()
        self.dao_collector = MockDaoCollector.build_from_env()
        api = WsInterface(self.dao_collector, self.AUTHORIZED_APIKEY)
        api.get_application().testing = True
        self.client = api.get_application().test_client()

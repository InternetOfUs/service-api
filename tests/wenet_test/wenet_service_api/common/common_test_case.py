from __future__ import absolute_import, annotations

from unittest import TestCase

from tests.wenet_test.wenet_service_api.common.mocks.mock_service_connector_collector import \
    MockServiceConnectorCollector
from wenet.wenet_service_api.ws.ws import WsInterface


class CommonTestCase(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.service_collector_connector = MockServiceConnectorCollector.build()
        api = WsInterface(self.service_collector_connector)
        api.get_application().testing = True
        self.client = api.get_application().test_client()

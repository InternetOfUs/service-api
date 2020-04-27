from __future__ import absolute_import, annotations

from unittest import TestCase

from tests.wenet_service_api_test.api.common.mocks.mock_dao_collector import MockDaoCollector
from tests.wenet_service_api_test.api.common.mocks.mock_service_connector_collector import MockServiceConnectorCollector
from wenet_service_api.api.ws.ws import WsInterface


class CommonTestCase(TestCase):

    AUTHORIZED_APIKEY = "1234"

    def setUp(self) -> None:
        super().setUp()
        self.service_collector_connector = MockServiceConnectorCollector.build()
        self.dao_collector = MockDaoCollector.build_from_env()
        api = WsInterface(self.service_collector_connector, self.dao_collector, self.AUTHORIZED_APIKEY)
        api.get_application().testing = True
        self.client = api.get_application().test_client()

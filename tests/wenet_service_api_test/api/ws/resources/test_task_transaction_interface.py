from __future__ import absolute_import, annotations

from mock import Mock

from tests.wenet_service_api_test.api.common.common_test_case import CommonTestCase
from wenet.common.model.task.transaction import TaskTransaction
from wenet_service_api.api.ws.resource.common import WenetSource


class TestTaskTransactionInterface(CommonTestCase):

    def test_post(self):

        task_transaction = TaskTransaction("id", "taskId", "label", 12, 100, "actioner id", {"key": "value"}, [])

        mock_post = Mock()

        self.service_collector_connector.task_manager_connector.post_task_transaction = mock_post

        response = self.client.post("/task/transaction", json=task_transaction.to_repr(), headers={"apikey": self.AUTHORIZED_APIKEY, "x-wenet-source": WenetSource.COMPONENT.value})
        self.assertEqual(response.status_code, 201)
        mock_post.assert_called_once()

    def test_post_not_authenticated(self):

        task_transaction = TaskTransaction("id", "taskId", "label", 12, 100, "actioner id", {"key": "value"}, [])

        mock_post = Mock()

        self.service_collector_connector.task_manager_connector.post_task_transaction = mock_post

        response = self.client.post("/task/transaction", json=task_transaction.to_repr())
        self.assertEqual(response.status_code, 401)

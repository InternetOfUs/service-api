from __future__ import absolute_import, annotations

from tests.wenet_service_api_test.api.common.common_test_case import CommonTestCase
from wenet.common.model.task.task import TaskAttribute
from wenet.common.model.task.transaction import TaskTransaction


class TestTaskTransactionInterface(CommonTestCase):

    def test_post(self):

        task_transaction = TaskTransaction("taskId", TaskTransaction.LABEL_ACCEPT_VOLUNTEER, [TaskAttribute("name", "value")])

        response = self.client.post("/task/transaction", json=task_transaction.to_repr(), headers={"apikey": self.AUTHORIZED_APIKEY})
        self.assertEqual(response.status_code, 201)

    def test_post_not_authenticated(self):

        task_transaction = TaskTransaction("taskId", TaskTransaction.LABEL_ACCEPT_VOLUNTEER, [TaskAttribute("name", "value")])

        response = self.client.post("/task/transaction", json=task_transaction.to_repr())
        self.assertEqual(response.status_code, 403)

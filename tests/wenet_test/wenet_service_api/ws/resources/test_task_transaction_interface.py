from __future__ import absolute_import, annotations

import json

from mock import Mock

from tests.wenet_test.wenet_service_api.common.common_test_case import CommonTestCase
from wenet.model.task import TaskAttribute
from wenet.model.task_transaction import TaskTransaction


class TestTaskTransactionInterface(CommonTestCase):

    def test_post(self):

        task_transaction = TaskTransaction("taskId", "typeId", [TaskAttribute("name", "value")])

        response = self.client.post("/task_transaction", json=task_transaction.to_repr(), headers={"apikey": self.AUTHORIZED_APIKEY})
        self.assertEqual(response.status_code, 201)

    def test_post_not_authenticated(self):

        task_transaction = TaskTransaction("taskId", "typeId", [TaskAttribute("name", "value")])

        response = self.client.post("/task_transaction", json=task_transaction.to_repr())
        self.assertEqual(response.status_code, 403)

from __future__ import absolute_import, annotations

import json

from tests.wenet_test.wenet_service_api.common.common_test_case import CommonTestCase
from wenet.model.norm import Norm, NormOperator
from wenet.model.task import Task, TaskState


class TestTaskInterface(CommonTestCase):

    def test_get(self):
        task_id = "task-id"
        response = self.client.get("/task/%s" % task_id, headers={"apikey": self.AUTHORIZED_APIKEY})
        self.assertEqual(response.status_code, 200)

    def test_get_not_authorized(self):
        task_id = "task-id"
        response = self.client.get("/task/%s" % task_id)
        self.assertEqual(response.status_code, 403)

    def test_put(self):
        task_id = "task-id"
        task = Task(
            task_id="task-id",
            creation_ts=1577833200,
            state=TaskState.ASSIGNED,
            requester_user_id="req_user_id",
            start_ts=1577833100,
            end_ts=1577833300,
            deadline_ts=1577833350,
            norms=[
                Norm(
                    norm_id="norm-id",
                    attribute="attribute",
                    operator=NormOperator.EQUALS,
                    comparison=True,
                    negation=False
                )
            ]
        )

        response = self.client.put("/task/%s" % task_id, json=task.to_repr(), headers={"apikey": self.AUTHORIZED_APIKEY})
        self.assertEqual(response.status_code, 200)

        json_data = json.loads(response.data)

        task = Task.from_repr(json_data)

        self.assertIsInstance(task, Task)

    def test_put_not_authorized(self):
        task_id = "task-id"
        task = Task(
            task_id="task-id",
            creation_ts=1577833200,
            state=TaskState.ASSIGNED,
            requester_user_id="req_user_id",
            start_ts=1577833100,
            end_ts=1577833300,
            deadline_ts=1577833350,
            norms=[
                Norm(
                    norm_id="norm-id",
                    attribute="attribute",
                    operator=NormOperator.EQUALS,
                    comparison=True,
                    negation=False
                )
            ]
        )

        response = self.client.put("/task/%s" % task_id, json=task.to_repr())
        self.assertEqual(response.status_code, 403)

    def test_put_wrong(self):
        task_id = "task-id"
        task = Task(
            task_id="task-id",
            creation_ts=1577833200,
            state=TaskState.ASSIGNED,
            requester_user_id="req_user_id",
            start_ts=1577833100,
            end_ts=1577833300,
            deadline_ts=1577833350,
            norms=[
                Norm(
                    norm_id="norm-id",
                    attribute="attribute",
                    operator=NormOperator.EQUALS,
                    comparison=True,
                    negation=False
                )
            ]
        )

        data = task.to_repr()
        data.pop("norms")
        response = self.client.put("/task/%s" % task_id, json=data, headers={"apikey": self.AUTHORIZED_APIKEY})
        self.assertEqual(response.status_code, 400)


class TestTaskPostInterface(CommonTestCase):

    def test_post(self):
        task = Task(
            task_id="task-id",
            creation_ts=1577833200,
            state=TaskState.ASSIGNED,
            requester_user_id="req_user_id",
            start_ts=1577833100,
            end_ts=1577833300,
            deadline_ts=1577833350,
            norms=[
                Norm(
                    norm_id="norm-id",
                    attribute="attribute",
                    operator=NormOperator.EQUALS,
                    comparison=True,
                    negation=False
                )
            ]
        )

        response = self.client.post("/task", json=task.to_repr(), headers={"apikey": self.AUTHORIZED_APIKEY})
        self.assertEqual(response.status_code, 201)

        json_data = json.loads(response.data)

        task = Task.from_repr(json_data)

        self.assertIsInstance(task, Task)


    def test_post(self):
        task = Task(
            task_id="task-id",
            creation_ts=1577833200,
            state=TaskState.ASSIGNED,
            requester_user_id="req_user_id",
            start_ts=1577833100,
            end_ts=1577833300,
            deadline_ts=1577833350,
            norms=[
                Norm(
                    norm_id="norm-id",
                    attribute="attribute",
                    operator=NormOperator.EQUALS,
                    comparison=True,
                    negation=False
                )
            ]
        )

        response = self.client.post("/task", json=task.to_repr())
        self.assertEqual(response.status_code, 403)

    def test_post_wrong(self):
        task = Task(
            task_id="task-id",
            creation_ts=1577833200,
            state=TaskState.ASSIGNED,
            requester_user_id="req_user_id",
            start_ts=1577833100,
            end_ts=1577833300,
            deadline_ts=1577833350,
            norms=[
                Norm(
                    norm_id="norm-id",
                    attribute="attribute",
                    operator=NormOperator.EQUALS,
                    comparison=True,
                    negation=False
                )
            ]
        )

        data = task.to_repr()
        data.pop("norms")
        response = self.client.post("/task", json=data, headers={"apikey": self.AUTHORIZED_APIKEY})
        self.assertEqual(response.status_code, 400)


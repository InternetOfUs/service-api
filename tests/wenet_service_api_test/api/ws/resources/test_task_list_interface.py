from __future__ import absolute_import, annotations

import json

from mock import Mock

from tests.wenet_service_api_test.api.common.common_test_case import CommonTestCase
from wenet.common.model.norm.norm import Norm, NormOperator
from wenet.common.model.task.task import TaskPage, Task, TaskGoal
from wenet_service_api.api.ws.resource.common import WenetSource


class TestTaskListInterface(CommonTestCase):

    def test_get(self):
        task_id = "task-id"
        task_page = TaskPage(
            offset=1,
            total=100,
            tasks=[
                Task(
                    task_id="task-id",
                    creation_ts=1577833200,
                    last_update_ts=1577833200,
                    task_type_id="task_type_id",
                    requester_id="requester_id",
                    app_id="app_id",
                    goal=TaskGoal(
                        name="goal",
                        description="description"
                    ),
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
                    ],
                    attributes={
                        "key": "value"
                    }
                ),
                Task(
                    task_id="task-id1",
                    creation_ts=1577833200,
                    last_update_ts=1577833200,
                    task_type_id="task_type_id",
                    requester_id="requester_id",
                    app_id="app_id",
                    goal=TaskGoal(
                        name="goal",
                        description="description"
                    ),
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
                    ],
                    attributes={
                        "key": "value"
                    }
                )
            ]
        )

        mock_get = Mock(return_value=task_page)
        self.service_collector_connector.task_manager_connector.get_task = mock_get
        response = self.client.get("/task/%s" % task_id, headers={"apikey": self.AUTHORIZED_APIKEY, "x-wenet-source": WenetSource.COMPONENT.value})

        self.assertEqual(response.status_code, 200)
        mock_get.assert_called_once()
        json_data = json.loads(response.data)

        from_repr = TaskPage.from_repr(json_data)
        self.assertEqual(from_repr, task_page)

    def test_get_not_authorized(self):
        response = self.client.get("/tasks")
        self.assertEqual(response.status_code, 401)

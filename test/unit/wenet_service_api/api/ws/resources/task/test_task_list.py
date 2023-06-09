from __future__ import absolute_import, annotations

import json

from mock import Mock

from wenet.model.task.task import TaskPage, Task, TaskGoal

from test.unit.wenet_service_api.api.common.common_test_case import CommonTestCase
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
                    norms=[
                        {
                            "description": "Notify to all the participants that the task is closed.",
                            "whenever": "is_received_do_transaction('close',Reason) and not(is_task_closed()) and get_profile_id(Me) and get_task_requester_id(RequesterId) and =(Me,RequesterId) and get_participants(Participants)",
                            "thenceforth": "add_message_transaction() and close_task() and send_messages(Participants,'close',Reason)",
                            "ontology": "get_participants(P) :- get_task_state_attribute(UserIds,'participants',[]), get_profile_id(Me), wenet_remove(P,Me,UserIds)."
                        }
                    ],
                    attributes={
                        "key": "value"
                    },
                    community_id="community_id",
                    close_ts=None,
                    transactions=[]
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
                    norms=[
                        {
                            "description": "Notify to all the participants that the task is closed.",
                            "whenever": "is_received_do_transaction('close',Reason) and not(is_task_closed()) and get_profile_id(Me) and get_task_requester_id(RequesterId) and =(Me,RequesterId) and get_participants(Participants)",
                            "thenceforth": "add_message_transaction() and close_task() and send_messages(Participants,'close',Reason)",
                            "ontology": "get_participants(P) :- get_task_state_attribute(UserIds,'participants',[]), get_profile_id(Me), wenet_remove(P,Me,UserIds)."
                        }
                    ],
                    attributes={
                        "key": "value"
                    },
                    community_id="community_id",
                    close_ts=None,
                    transactions=[]
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

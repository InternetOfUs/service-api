from __future__ import absolute_import, annotations

import json

from mock import Mock

from wenet.model.task.task import Task, TaskGoal

from test.unit.wenet_service_api.api.common.common_test_case import CommonTestCase
from wenet_service_api.api.ws.resource.common import WenetSource


class TestTaskInterface(CommonTestCase):

    def test_get(self):
        task_id = "task-id"
        task = Task(
            task_id="task-id",
            creation_ts=1577833200,
            last_update_ts=1577833200,
            task_type_id="task_type_id",
            requester_id="requester_id",
            app_id="app_id",
            community_id="community_id",
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
            close_ts=None,
            transactions=[]
        )

        mock_get = Mock(return_value=task)
        self.service_collector_connector.task_manager_connector.get_task = mock_get
        response = self.client.get("/task/%s" % task_id, headers={"apikey": self.AUTHORIZED_APIKEY, "x-wenet-source": WenetSource.COMPONENT.value})

        self.assertEqual(response.status_code, 200)
        mock_get.assert_called_once()
        json_data = json.loads(response.data)

        from_repr = Task.from_repr(json_data)
        self.assertEqual(from_repr, task)

    def test_get_not_authorized(self):
        task_id = "task-id"
        response = self.client.get("/task/%s" % task_id)
        self.assertEqual(response.status_code, 401)

    def test_put(self):
        task_id = "task-id"
        task = Task(
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

        )

        mock_put = Mock(return_value=task)
        self.service_collector_connector.task_manager_connector.update_task = mock_put

        response = self.client.put("/task/%s" % task_id, json=task.to_repr(), headers={"apikey": self.AUTHORIZED_APIKEY, "x-wenet-source": WenetSource.COMPONENT.value})
        self.assertEqual(response.status_code, 200)

        json_data = json.loads(response.data)

        task = Task.from_repr(json_data)

        self.assertIsInstance(task, Task)
        mock_put.assert_called_once()

    def test_put_invalid_json(self):
        task_id = "task-id"

        mock_put = Mock()
        self.service_collector_connector.task_manager_connector.update_task = mock_put

        response = self.client.put("/task/%s" % task_id, data='{invalid_json', headers={"apikey": self.AUTHORIZED_APIKEY, "x-wenet-source": WenetSource.COMPONENT.value, "Content-Type": "application/json"})
        self.assertEqual(response.status_code, 400)

        mock_put.assert_not_called()

    def test_put_no_json(self):
        task_id = "task-id"

        mock_put = Mock()
        self.service_collector_connector.task_manager_connector.update_task = mock_put

        response = self.client.put("/task/%s" % task_id, data='invalid_json', headers={"apikey": self.AUTHORIZED_APIKEY, "x-wenet-source": WenetSource.COMPONENT.value})
        self.assertEqual(response.status_code, 400)

        mock_put.assert_not_called()

    def test_put_not_authorized(self):
        task_id = "task-id"
        task = Task(
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
        )

        response = self.client.put("/task/%s" % task_id, json=task.to_repr())
        self.assertEqual(response.status_code, 401)

    def test_put_wrong(self):
        task_id = "task-id"
        task = Task(
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
        )

        data = task.to_repr()
        data["norms"] = "text"

        mock_put = Mock()
        self.service_collector_connector.task_manager_connector.get_task = mock_put

        response = self.client.put("/task/%s" % task_id, json=data, headers={"apikey": self.AUTHORIZED_APIKEY, "x-wenet-source": WenetSource.COMPONENT.value})
        self.assertEqual(response.status_code, 400)

        mock_put.assert_not_called()


class TestTaskPostInterface(CommonTestCase):

    def test_post(self):
        task = Task(
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
        )

        mock_post = Mock(return_value=task)
        self.service_collector_connector.task_manager_connector.create_task = mock_post

        response = self.client.post("/task", json=task.to_repr(), headers={"apikey": self.AUTHORIZED_APIKEY, "x-wenet-source": WenetSource.COMPONENT.value})
        self.assertEqual(response.status_code, 201)

        json_data = json.loads(response.data)

        created_task = Task.from_repr(json_data)

        self.assertIsInstance(created_task, Task)
        # self.assertNotEqual(task.task_id, created_task.task_id)
        mock_post.assert_called_once()

    def test_post2(self):
        task = Task(
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
        )

        response = self.client.post("/task", json=task.to_repr())
        self.assertEqual(response.status_code, 401)

    def test_post_wrong(self):
        task = Task(
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
        )

        mock_post = Mock()
        self.service_collector_connector.task_manager_connector.create_task = mock_post

        data = task.to_repr()
        data["norms"] = "text"
        response = self.client.post("/task", json=data, headers={"apikey": self.AUTHORIZED_APIKEY, "x-wenet-source": WenetSource.COMPONENT.value})
        self.assertEqual(response.status_code, 400)
        mock_post.assert_not_called()

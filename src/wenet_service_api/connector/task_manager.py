from __future__ import absolute_import, annotations

import json
import os
from typing import Optional

import requests

from wenet.common.model.norm.norm import Norm, NormOperator
from wenet.common.model.task.task import Task, TaskGoal, TaskPage
from wenet.common.model.task.transaction import TaskTransaction
from wenet_service_api.common.exception.exceptions import ResourceNotFound, NotAuthorized, BadRequestException
from wenet_service_api.connector.service_connector import ServiceConnector


class TaskManagerConnector(ServiceConnector):

    def __init__(self, base_url: str, base_headers: Optional[dict] = None):
        super().__init__(base_url, base_headers)

    @staticmethod
    def build_from_env() -> TaskManagerConnector:

        base_url = os.getenv("TASK_MANAGER_CONNECTOR_BASE_URL")

        if not base_url:
            raise RuntimeError("ENV: TASK_MANAGER_CONNECTOR_BASE_URL is not defined")

        return TaskManagerConnector(
            base_url=base_url,
            base_headers={
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
        )

    def get_task(self, task_id: str, headers: Optional[dict] = None) -> Task:
        url = f"{self._base_url}/tasks/{task_id}"

        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return Task.from_repr(response.json())
        elif response.status_code == 404:
            raise ResourceNotFound(f"Unable to found a task with id [{task_id}]")
        elif response.status_code == 401 or response.status_code == 403:
            raise NotAuthorized("Not authorized")
        else:
            raise Exception(f"Unable to found a task with id [{task_id}], server respond [{response.status_code}] [{response.text}]")

    def get_tasks(self,
                  app_id: Optional[str] = None,
                  requester_id: Optional[str] = None,
                  task_type_id: Optional[str] = None,
                  goal_name: Optional[str] = None,
                  goal_description: Optional[str] = None,
                  start_from: Optional[int] = None,
                  start_to: Optional[int] = None,
                  end_from: Optional[int] = None,
                  end_to: Optional[int] = None,
                  deadline_from: Optional[int] = None,
                  deadline_to: Optional[int] = None,
                  offset: Optional[int] = None,
                  limit: Optional[int] = None,
                  headers: Optional[dict] = None
                  ) -> TaskPage:
        url = f"{self._base_url}/tasks"

        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        query_params_temp = {
            "appId": app_id,
            "requesterId": requester_id,
            "taskTypeId": task_type_id,
            "goalName": goal_name,
            "goalDescription": goal_description,
            "startFrom": start_from,
            "startTo": start_to,
            "endFrom": end_from,
            "endTo": end_to,
            "deadlineFrom": deadline_from,
            "deadlineTo": deadline_to,
            "offset": offset,
            "limit": limit
        }

        query_params = {}

        for key in query_params_temp:
            if query_params_temp[key] is not None:
                query_params[key] = query_params_temp[key]

        response = requests.get(url, params=query_params)

        if response.status_code == 200:
            return TaskPage.from_repr(response.json())
        elif response.status_code == 401 or response.status_code == 403:
            raise NotAuthorized("Not authorized")
        else:
            raise Exception(f"Unable to retrive the task list with the following parameters {query_params}")

    def create_task(self, task: Task, headers: Optional[dict] = None) -> Task:
        url = f"{self._base_url}/tasks"

        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        task_repr = task.prepare_task()
        task_repr.pop("id", None)
        # task_repr.pop("requesterUserId", None)
        json_data = json.dumps(task_repr)
        response = requests.post(url, headers=headers, data=json_data)

        if response.status_code == 200:
            task = Task.from_repr(response.json())
        elif response.status_code == 401 or response.status_code == 403:
            raise NotAuthorized("Not authorized")
        elif response.status_code == 400:
            raise BadRequestException(f"Bad request {response.text}")
        else:
            raise Exception(f"Unable to create the task, server respond with [{response.status_code}] [{response.text}]")

        return task

    def updated_task(self, task: Task, headers: Optional[dict] = None) -> Task:
        url = f"{self._base_url}/tasks/{task.task_id}"

        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        task_repr = task.prepare_task()

        json_data = json.dumps(task_repr)

        response = requests.put(url, headers=headers, data=json_data)

        if response.status_code == 200:
            return Task.from_repr(response.json())
        elif response.status_code == 401 or response.status_code == 403:
            raise NotAuthorized(f"Not authorized {response.text}")
        elif response.status_code == 404:
            raise ResourceNotFound(f"Resource [{task.task_id}] not found on resource manager")
        elif response.status_code == 400:
            raise BadRequestException(f"Bad request {response.text}")
        else:
            raise Exception(f"Unable to edit the task [{task.task_id}], server respond with [{response.status_code}] [{response.text}]")

    def post_task_transaction(self, task_transaction: TaskTransaction, headers: Optional[dict] = None):
        url = f"{self._base_url}/tasks/transactions"

        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        json_data = json.dumps(task_transaction.to_repr())

        response = requests.post(url, headers=headers, data=json_data)

        if response.status_code == 200:
            return
        elif response.status_code == 401 or response.status_code == 403:
            raise NotAuthorized(f"Not authorized {response.text}")
        elif response.status_code == 400:
            raise BadRequestException(f"Bad request {response.text}")
        else:
            raise Exception(f"Unable to post the task transaction [{task_transaction}], server respond with [{response.status_code}] [{response.text}]")


class DummyTaskManagerConnector(TaskManagerConnector):

    def __init__(self):
        super().__init__("")

    @staticmethod
    def build_from_env() -> TaskManagerConnector:
        return DummyTaskManagerConnector()

    def get_task(self, task_id: str, headers: Optional[dict] = None) -> Task:
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
        return task

    def get_tasks(self, app_id: Optional[str] = None, requester_id: Optional[str] = None,
                  task_type_id: Optional[str] = None, goal_name: Optional[str] = None,
                  goal_description: Optional[str] = None, start_from: Optional[int] = None,
                  start_to: Optional[int] = None, end_from: Optional[int] = None, end_to: Optional[int] = None,
                  deadline_from: Optional[int] = None, deadline_to: Optional[int] = None, offset: Optional[int] = None,
                  limit: Optional[int] = None, headers: Optional[dict] = None) -> TaskPage:
        return TaskPage(
            offset=offset,
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

    def create_task(self, task: Task, headers: Optional[dict] = None) -> Task:
        return task

    def updated_task(self, task: Task, headers: Optional[dict] = None) -> Task:
        return task

    def post_task_transaction(self, task_transaction: TaskTransaction, headers: Optional[dict] = None):
        return

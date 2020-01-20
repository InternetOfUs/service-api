from __future__ import absolute_import, annotations

from unittest import TestCase

from wenet.model.norm import Norm, NormOperator
from wenet.model.task import Task, TaskState


class TestTask(TestCase):

    def test_repr(self):

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

        to_repr = task.to_repr()
        from_repr = Task.from_repr(to_repr)

        self.assertEqual(task, from_repr)

    def test_equals(self):
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
        task1 = Task(
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
        task2 = Task(
            task_id="task-id1",
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
        task3 = Task(
            task_id="task-id",
            creation_ts=1577833201,
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
        task4 = Task(
            task_id="task-id",
            creation_ts=1577833200,
            state=TaskState.COMPLETED,
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
        task5 = Task(
            task_id="task-id",
            creation_ts=1577833200,
            state=TaskState.ASSIGNED,
            requester_user_id="req_user_id1",
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
        task6 = Task(
            task_id="task-id",
            creation_ts=1577833200,
            state=TaskState.ASSIGNED,
            requester_user_id="req_user_id",
            start_ts=1577833101,
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
        task7 = Task(
            task_id="task-id",
            creation_ts=1577833200,
            state=TaskState.ASSIGNED,
            requester_user_id="req_user_id",
            start_ts=1577833100,
            end_ts=1577833301,
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
        task8 = Task(
            task_id="task-id",
            creation_ts=1577833200,
            state=TaskState.ASSIGNED,
            requester_user_id="req_user_id",
            start_ts=1577833100,
            end_ts=1577833300,
            deadline_ts=1577833351,
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
        task9 = Task(
            task_id="task-id",
            creation_ts=1577833200,
            state=TaskState.ASSIGNED,
            requester_user_id="req_user_id",
            start_ts=1577833100,
            end_ts=1577833300,
            deadline_ts=1577833350,
            norms=[
                Norm(
                    norm_id="norm-id1",
                    attribute="attribute",
                    operator=NormOperator.EQUALS,
                    comparison=True,
                    negation=False
                )
            ]
        )

        self.assertEqual(task, task1)
        self.assertNotEqual(task, task2)
        self.assertNotEqual(task, task3)
        self.assertNotEqual(task, task4)
        self.assertNotEqual(task, task5)
        self.assertNotEqual(task, task6)
        self.assertNotEqual(task, task7)
        self.assertNotEqual(task, task8)
        self.assertNotEqual(task, task9)

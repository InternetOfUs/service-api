from __future__ import absolute_import, annotations

from enum import Enum
from numbers import Number
from typing import Optional, List

from wenet_service_api.model.norm import Norm


class TaskState(Enum):

    OPEN = "Open"
    PENDING_ASSIGNMENT = "PendingAssignment"
    ASSIGNED = "Assigned"
    COMPLETED = "Completed"
    EXPIRED = "Expired"
    CANCELLED = "Cancelled"


class TaskGoal:

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def to_repr(self) -> dict:
        return {
            "name": self.name,
            "description": self.description
        }

    @staticmethod
    def from_repr(raw_data: dict) -> TaskGoal:
        return TaskGoal(
            name=raw_data["name"],
            description=raw_data["description"]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, TaskGoal):
            return False

        return self.name == o.name and self.description == o.description

    def __repr__(self) -> str:
        return str(self.to_repr())

    def __str__(self):
        return self.to_repr()


class TaskAttribute:

    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value

    def to_repr(self) -> dict:
        return {
            "name": self.name,
            "value": self.value
        }

    @staticmethod
    def from_repr(raw_data: dict) -> TaskAttribute:
        return TaskAttribute(
            name=raw_data["name"],
            value=raw_data["value"]
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, TaskAttribute):
            return False
        return self.name == o.name and self.value == o.value

    def __repr__(self) -> str:
        return str(self.to_repr())

    def __str__(self) -> str:
        return self.__repr__()


class Task:

    def __init__(self,
                 task_id: str,
                 creation_ts: Number,
                 last_update_ts: Number,
                 task_type_id: str,
                 requester_id: str,
                 app_id: str,
                 goal: TaskGoal,
                 start_ts: Number,
                 end_ts: Number,
                 deadline_ts: Number,
                 norms: Optional[List[Norm]],
                 attributes: Optional[List[TaskAttribute]]
                 ):

        self.task_id = task_id
        self.creation_ts = creation_ts

        self.last_update_ts = last_update_ts
        self.task_type_id = task_type_id
        self.requester_id = requester_id
        self.app_id = app_id
        self.goal = goal

        self.start_ts = start_ts
        self.end_ts = end_ts
        self.deadline_ts = deadline_ts
        self.norms = norms

        self.attributes = attributes

        if not isinstance(task_id, str):
            raise TypeError("TaskId should be a string")
        if not isinstance(creation_ts, Number):
            raise TypeError("CreationTs should be a string")

        if not isinstance(last_update_ts, Number):
            raise TypeError("LastUpdateTs should be a number")

        if not isinstance(task_type_id, str):
            raise TypeError("TaskType Id should be a string")

        if not isinstance(requester_id, str):
            raise TypeError("RequesterId Id should be a string")

        if not isinstance(app_id, str):
            raise TypeError("AppId should be a string")

        if not isinstance(goal, TaskGoal):
            raise TypeError("Goal should be an instance of TaskGoal")

        if start_ts is not None:
            if not isinstance(start_ts, Number):
                raise TypeError("StartTs should be an integer")

        if end_ts is not None:
            if not isinstance(end_ts, Number):
                raise TypeError("EndTs should be an integer")

        if deadline_ts is not None:
            if not isinstance(deadline_ts, Number):
                raise TypeError("DeadlineTs should be an integer")

        if norms:
            if not isinstance(norms, list):
                raise ValueError("Norms should be a list of Norm")
            else:
                for norm in norms:
                    if not isinstance(norm, Norm):
                        raise ValueError("Norms should be a list of Norm")
        else:
            self.norms = []

        if attributes:
            if not isinstance(attributes, list):
                raise TypeError("Attributes should be a list of attributes")
            else:
                for attribute in attributes:
                    if not isinstance(attribute, TaskAttribute):
                        raise TypeError("Attributes should be a list of attributes")
        else:
            self.attributes = []

    def to_repr(self) -> dict:
        return {
            "taskId": self.task_id,
            "_creationTs": self.creation_ts,
            "_lastUpdateTs": self.last_update_ts,
            "taskTypeId": self.task_type_id,
            "requesterId": self.requester_id,
            "appId": self.app_id,
            "goal": self.goal.to_repr(),
            "startTs": self.start_ts,
            "endTs": self.end_ts,
            "deadlineTs": self.deadline_ts,
            "norms": list(x.to_repr() for x in self.norms),
            "attributes": list(x.to_repr() for x in self.attributes)
        }

    @staticmethod
    def from_repr(raw_data: dict, task_id: Optional[str] = None) -> Task:

        if task_id is None:
            task_id = raw_data["taskId"]

        return Task(
            task_id=task_id,
            creation_ts=raw_data.get("_creationTs"),
            last_update_ts=raw_data["_lastUpdateTs"],
            task_type_id=raw_data["taskTypeId"],
            requester_id=raw_data["requesterId"],
            app_id=raw_data["appId"],
            goal=TaskGoal.from_repr(raw_data["goal"]),
            start_ts=raw_data.get("startTs", None),
            end_ts=raw_data.get("endTs", None),
            deadline_ts=raw_data.get("deadlineTs", None),
            norms=list(Norm.from_repr(x) for x in raw_data["norms"]) if raw_data.get("norms", None) else None,
            attributes=list(TaskAttribute.from_repr(x) for x in raw_data["attributes"]) if raw_data.get("attributes", None) else None
        )

    def __repr__(self):
        return str(self.to_repr())

    def __str__(self):
        return self.__repr__()

    def __eq__(self, o):
        if not isinstance(o, Task):
            return False
        return self.task_id == o.task_id and self.creation_ts == o.creation_ts and self.last_update_ts == o.last_update_ts and self.task_type_id == o.task_type_id \
            and self.requester_id == o.requester_id and self.app_id == o.app_id and self.goal == o.goal and self.start_ts == o.start_ts \
            and self.end_ts == o.end_ts and self.deadline_ts == o.deadline_ts and self.norms == o.norms and self.attributes == o.attributes

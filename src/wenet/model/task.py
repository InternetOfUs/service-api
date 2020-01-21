from __future__ import absolute_import, annotations

from enum import Enum
from numbers import Number
from typing import Optional, List

from wenet.model.norm import Norm


class TaskState(Enum):

    OPEN = "Open"
    PENDING_ASSIGNMENT = "PendingAssignment"
    ASSIGNED = "Assigned"
    COMPLETED = "Completed"
    EXPIRED = "Expired"
    CANCELLED = "Cancelled"


class Task:

    def __init__(self,
                 task_id: str,
                 creation_ts: Optional[Number],
                 state: Optional[TaskState],
                 requester_user_id: Optional[str],
                 start_ts: Optional[Number],
                 end_ts: Optional[Number],
                 deadline_ts: Optional[Number],
                 norms: List[Norm]
                 ):

        self.task_id = task_id
        self.creation_ts = creation_ts
        self.state = state
        self.requester_user_id = requester_user_id
        self.start_ts = start_ts
        self.end_ts = end_ts
        self.deadline_ts = deadline_ts
        self.norms = norms

        if not isinstance(task_id, str):
            raise TypeError("TaskId should be a string")
        if creation_ts is not None:
            if not isinstance(creation_ts, Number):
                raise TypeError("CreationTs should be a string")
        if state:
            if not isinstance(state, TaskState):
                raise TypeError("State should be a TaskState")
        if requester_user_id:
            if not isinstance(requester_user_id, str):
                raise TypeError("RequestUserId should be a string")
        if start_ts is not None:
            if not isinstance(start_ts, Number):
                raise TypeError("StartTs should be an integer")
        if end_ts is not None:
            if not isinstance(end_ts, Number):
                raise TypeError("EndTs should be an integer")
        if deadline_ts is not None:
            if not isinstance(deadline_ts, Number):
                raise TypeError("DeadlineTs should be an integer")

        if not isinstance(norms, list):
            raise ValueError("Norms should be a list of Norm")
        else:
            for norm in norms:
                if not isinstance(norm, Norm):
                    raise ValueError("Norms should be a list of Norm")

    def to_repr(self) -> dict:
        return {
            "taskId": self.task_id,
            "creationTs": self.creation_ts,
            "state": self.state.value,
            "requesterUserId": self.requester_user_id,
            "startTs": self.start_ts,
            "endTs": self.end_ts,
            "deadlineTs": self.deadline_ts,
            "norms": list(x.to_repr() for x in self.norms)
        }

    @staticmethod
    def from_repr(raw_data: dict) -> Task:
        return Task(
            task_id=raw_data["taskId"],
            creation_ts=raw_data.get("creationTs"),
            state=TaskState(raw_data["state"]) if raw_data.get("state", None) else None,
            requester_user_id=raw_data.get("requesterUserId", None),
            start_ts=raw_data.get("startTs", None),
            end_ts=raw_data.get("endTs", None),
            deadline_ts=raw_data.get("deadlineTs", None),
            norms=list(Norm.from_repr(x) for x in raw_data["norms"])
        )

    def __repr__(self):
        return str(self.to_repr())

    def __str__(self):
        return self.__repr__()

    def __eq__(self, o):
        if not isinstance(o, Task):
            return False
        return self.task_id == o.task_id and self.creation_ts == o.creation_ts and self.state == o.state and self.requester_user_id == o.requester_user_id \
            and self.start_ts == o.start_ts and self.end_ts == o.end_ts and self.deadline_ts == o.deadline_ts and self.norms == o.norms

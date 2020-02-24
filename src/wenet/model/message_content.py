from __future__ import absolute_import, annotations

import abc
from enum import Enum


class MessageContentType(Enum):

    TEXTUAL_MESSAGE = "textual_message"
    ACTION_REQUEST = "action_request"


class MessageContent(abc.ABC):

    @staticmethod
    @abc.abstractmethod
    def get_type() -> MessageContentType:
        pass

    @abc.abstractmethod
    def to_repr(self) -> dict:
        pass

    def base_repr(self) -> dict:
        return {
            "type": self.get_type().value
        }

    @staticmethod
    def from_repr(raw_data: dict) -> MessageContent:

        message_type = MessageContentType(raw_data["type"])

        if message_type == TextualMessage.get_type():
            return TextualMessage.from_repr(raw_data)
        elif message_type == ActionRequest.get_type():
            return ActionRequest.from_repr(raw_data)
        else:
            raise ValueError(f"Unable to build a message from type {message_type.value}")

    def __eq__(self, o):
        if not isinstance(o, MessageContent):
            return False
        return self.get_type() == o.get_type()

    def __repr__(self) -> str:
        return str(self.to_repr())

    def __str__(self) -> str:
        return self.__repr__()


class TextualMessage(MessageContent):

    MESSAGE_TYPE = MessageContentType.TEXTUAL_MESSAGE

    def __init__(self, value: str):
        self.value = value

        if not isinstance(self.value, str):
            raise TypeError("Value should be a string")

    @staticmethod
    def get_type() -> MessageContentType:
        return TextualMessage.MESSAGE_TYPE

    def to_repr(self) -> dict:
        base_repr = self.base_repr()
        base_repr.update({
            "value": self.value
        })
        return base_repr

    @staticmethod
    def from_repr(raw_data: dict) -> TextualMessage:
        return TextualMessage(
            value=raw_data["value"]
        )

    def __eq__(self, o):
        if not isinstance(o, TextualMessage):
            return False
        return super().__eq__(o) and self.value == o.value


class ActionRequest(MessageContent):

    MESSAGE_TYPE = MessageContentType.ACTION_REQUEST

    def __init__(self, value: str, payload: str):
        self.value = value
        self.payload = payload

        if not isinstance(self.value, str):
            raise TypeError("Value should be a string")

        if not isinstance(self.payload, str):
            raise TypeError("Payload should be a string")

    @staticmethod
    def get_type() -> MessageContentType:
        return ActionRequest.MESSAGE_TYPE

    def to_repr(self) -> dict:
        base_repr = self.base_repr()
        base_repr.update({
            "value": self.value,
            "payload": self.payload
        })
        return base_repr

    @staticmethod
    def from_repr(raw_data: dict) -> ActionRequest:
        return ActionRequest(
            value=raw_data["value"],
            payload=raw_data["payload"]
        )

    def __eq__(self, o):
        if not isinstance(o, ActionRequest):
            return False
        return super().__eq__(o) and self.value == o.value and self.payload == o.payload

from __future__ import absolute_import, annotations

from enum import Enum
from typing import Optional, List

from iso639 import is_valid639_1

from wenet.model.message_content import MessageContent


class MessageType(Enum):

    REQUEST = "request"


class MessageIntent:

    def __init__(self, name: str, confidence: Optional[float]):
        self.name = name
        self.confidence = confidence

        if not isinstance(self.name, str):
            raise TypeError("Name should be a string")
        if self.confidence is not None:
            if not isinstance(self.confidence, float):
                raise TypeError("Confidence should be a float")

    def to_repr(self) -> dict:
        return {
            "name": self.name,
            "confidence": self.confidence
        }

    @staticmethod
    def from_repr(raw_data: dict) -> MessageIntent:
        return MessageIntent(
            name=raw_data["name"],
            confidence=raw_data.get("confidence", None)
        )

    def __eq__(self, o):
        if not isinstance(o, MessageIntent):
            return False
        return self.name == o.name and self.confidence == o.confidence

    def __repr__(self):
        return str(self.to_repr())

    def __str__(self):
        return self.__repr__()


class MessageEntity:

    def __init__(self, name: str, value: str, confidence: float):
        self.name = name
        self.value = value
        self.confidence = confidence

        if not isinstance(self.name, str):
            raise TypeError("Name should be a string")
        if not isinstance(self.value, str):
            raise TypeError("Value should be a string")
        if self.confidence is not None:
            if not isinstance(self.confidence, float):
                raise TypeError("Confidence should be a float")

    def to_repr(self) -> dict:
        return {
            "name": self.name,
            "value": self.value,
            "confidence": self.confidence
        }

    @staticmethod
    def from_repr(raw_data: dict) -> MessageEntity:
        return MessageEntity(
            name=raw_data["name"],
            value=raw_data["value"],
            confidence=raw_data.get("confidence", None)
        )

    def __eq__(self, o):
        if not isinstance(o, MessageEntity):
            return False
        return self.name == o.name and self.value == o.value and self.confidence == o.confidence

    def __repr__(self):
        return str(self.to_repr())

    def __str__(self):
        return self.__repr__()


class Message:

    def __init__(self,
                 message_id: str,
                 channel: str,
                 user_id: str,
                 app_id: str,
                 message_type: MessageType,
                 content: Optional[MessageContent],
                 domain: Optional[str],
                 intent: Optional[MessageIntent],
                 entities: Optional[List[MessageEntity]],
                 language: Optional[str],
                 metadata: Optional[dict]
                 ):

        self.message_id = message_id
        self.channel = channel
        self.user_id = user_id
        self.app_id = app_id
        self.message_type = message_type
        self.content = content
        self.domain = domain
        self.intent = intent
        self.entities = entities
        self.language = language
        self.metadata = metadata

        if self.entities is None:
            self.entities: List[MessageEntity] = []

        if self.metadata is None:
            self.metadata = {}

        if not isinstance(self.message_id, str):
            raise TypeError("MessageId should be a string")
        if not isinstance(self.channel, str):
            raise TypeError("Channel should be a string")
        if not isinstance(self.user_id, str):
            raise TypeError("UserId should be a string")
        if not isinstance(self.app_id, str):
            raise TypeError("AppId should be a string")
        if not isinstance(self.message_type, MessageType):
            raise TypeError("Message type should be a MessageType object")
        if self.content is not None:
            if not isinstance(self.content, MessageContent):
                raise TypeError("Content should be an instance of MessageContent")
        if self.domain is not None:
            if not isinstance(self.domain, str):
                raise TypeError("Domain should be a str")
        if self.intent is not None:
            if not isinstance(self.intent, MessageIntent):
                raise TypeError("intent should be an instance of MessageIntent")
        if self.entities is not None:
            if not isinstance(self.entities, list):
                raise TypeError("entities should be an list of MessageEntity")
            else:
                for entity in self.entities:
                    if not isinstance(entity, MessageEntity):
                        raise TypeError("entities should be an list of MessageEntity")
        if self.language is not None:
            if not isinstance(self.language, str):
                raise TypeError("Language should be a str")
            if not is_valid639_1(self.language):
                raise ValueError(f"Language {self.language} is not a valid ISO639-1 language code")
        if not isinstance(self.metadata, dict):
            raise TypeError("Metadata should be a dictionary")

    def to_repr(self) -> dict:
        return {
            "messageId": self.message_id,
            "channel": self.channel,
            "userId": self.user_id,
            "appId": self.app_id,
            "type": self.message_type.value,
            "content": self.content.to_repr() if self.content else None,
            "domain": self.domain,
            "intent": self.intent.to_repr() if self.intent else None,
            "entities": list(x.to_repr() for x in self.entities),
            "language": self.language,
            "metadata": self.metadata
        }

    @staticmethod
    def from_repr(raw_data: dict) -> Message:
        return Message(
            message_id=raw_data["messageId"],
            channel=raw_data["channel"],
            user_id=raw_data["userId"],
            app_id=raw_data["appId"],
            message_type=MessageType(raw_data["type"]),
            content=MessageContent.from_repr(raw_data["content"]) if raw_data.get("content", None) else None,
            domain=raw_data.get("domain", None),
            intent=MessageIntent.from_repr(raw_data["intent"]) if raw_data.get("intent", None) else None,
            entities=list(MessageEntity.from_repr(x) for x in raw_data["entities"]) if raw_data.get("entities", None) else None,
            language=raw_data.get("language", None),
            metadata=raw_data.get("metadata", None)
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Message):
            return False
        return self.message_id == o.message_id and self.channel == o.channel and self.user_id == o.user_id and self.app_id == o.app_id \
            and self.message_type == o.message_type and self.content == o.content and self.domain == o.domain and self.intent == o.intent \
            and self.entities == o.entities and self.language == o.language

    def __repr__(self) -> str:
        return str(self.to_repr())

    def __str__(self) -> str:
        return self.__repr__()

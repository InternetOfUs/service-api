from __future__ import absolute_import, annotations

from unittest import TestCase

from wenet.model.message import MessageIntent, MessageEntity, Message, MessageType
from wenet.model.message_content import TextualMessage


class TestMessageIntent(TestCase):

    def test_repr(self):
        message_intent = MessageIntent("name", 0.9)
        from_repr = MessageIntent.from_repr(message_intent.to_repr())

        self.assertIsInstance(from_repr, MessageIntent)
        self.assertEqual(message_intent, from_repr)

    def test_repr2(self):
        message_intent = MessageIntent("name", None)
        from_repr = MessageIntent.from_repr(message_intent.to_repr())

        self.assertIsInstance(from_repr, MessageIntent)
        self.assertEqual(message_intent, from_repr)


class TestMessageEntity(TestCase):

    def test_repr(self):
        message_entity = MessageEntity("name", "value", 0.9)
        from_repr = MessageEntity.from_repr(message_entity.to_repr())

        self.assertIsInstance(message_entity, MessageEntity)
        self.assertEqual(message_entity, from_repr)

    def test_repr2(self):
        message_entity = MessageEntity("name", "value", None)
        from_repr = MessageEntity.from_repr(message_entity.to_repr())

        self.assertIsInstance(message_entity, MessageEntity)
        self.assertEqual(message_entity, from_repr)


class TestMessage(TestCase):

    def test_repr(self):
        message = Message(
            message_id="message id",
            channel="channel",
            user_id="user_id",
            app_id="app_id",
            message_type=MessageType.REQUEST,
            content=TextualMessage(
                "value"
            ),
            domain="domain",
            intent=MessageIntent(
                "name",
                0.9
            ),
            entities=[
                MessageEntity(
                    "name",
                    "value",
                    0.9
                )
            ],
            language="it",
            metadata={}
        )

        from_repr = Message.from_repr(message.to_repr())

        self.assertIsInstance(from_repr, Message)
        self.assertEqual(message, from_repr)

    def test_repr2(self):
        message = Message(
            message_id="message id",
            channel="channel",
            user_id="user_id",
            app_id="app_id",
            message_type=MessageType.REQUEST,
            content=None,
            domain=None,
            intent=None,
            entities=None,
            language=None,
            metadata=None
        )

        self.assertEqual(message.entities, [])
        self.assertEqual(message.metadata, {})

        from_repr = Message.from_repr(message.to_repr())

        self.assertIsInstance(from_repr, Message)
        self.assertEqual(message, from_repr)

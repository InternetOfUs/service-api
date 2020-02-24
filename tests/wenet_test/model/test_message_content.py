from __future__ import absolute_import, annotations

from unittest import TestCase

from wenet.model.message_content import TextualMessage, MessageContent, ActionRequest


class TestTextualMessage(TestCase):

    def test_repr(self):
        textual_message = TextualMessage("value")

        from_repr = TextualMessage.from_repr(textual_message.to_repr())

        self.assertIsInstance(from_repr, TextualMessage)
        self.assertEqual(from_repr, textual_message)

        from_repr2 = MessageContent.from_repr(textual_message.to_repr())

        self.assertIsInstance(from_repr2, TextualMessage)
        self.assertEqual(from_repr2, textual_message)


class TestActionRequest(TestCase):

    def test_repr(self):
        action_request = ActionRequest("value", "payload")

        from_repr = ActionRequest.from_repr(action_request.to_repr())

        self.assertIsInstance(from_repr, ActionRequest)
        self.assertEqual(from_repr, action_request)

        from_repr2 = MessageContent.from_repr(action_request.to_repr())

        self.assertIsInstance(from_repr2, ActionRequest)
        self.assertEqual(from_repr2, action_request)

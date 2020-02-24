from __future__ import absolute_import, annotations

from tests.wenet_test.wenet_service_api.common.common_test_case import CommonTestCase
from wenet.model.message import Message, MessageType, MessageIntent, MessageEntity
from wenet.model.message_content import TextualMessage


class TestMessageInterface(CommonTestCase):

    def test_post(self):

        message = {
            "messageId": "message id",
            "channel": "channel",
            "userId": "user_id",
            "appId": "app_id",
            "type": "request",
            "content": {
                "type": "textual_message",
                "value": "value"
            },
            "domain": "domain",
            "intent": {
                "name": "name",
                "confidence": 0.9
            },
            "entities": [{
                "name": "name",
                "value": "value",
                "confidence": 0.9
            }],
            "language": "it",
            "metadata": {}
        }

        response = self.client.post("/messages", json=message)
        self.assertEqual(response.status_code, 201)

    def test_post2(self):

        message = {
            "channel": "channel",
            "userId": "user_id",
            "appId": "app_id",
            "type": "request",
            "content": {
                "type": "textual_message",
                "value": "value"
            },
            "domain": "domain",
            "intent": {
                "name": "name",
                "confidence": 0.9
            },
            "entities": [{
                "name": "name",
                "value": "value",
                "confidence": 0.9
            }],
            "language": "it",
            "metadata": {}
        }

        response = self.client.post("/messages", json=message)
        self.assertEqual(response.status_code, 400)

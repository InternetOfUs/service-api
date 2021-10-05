from __future__ import absolute_import, annotations

from test.unit.wenet_service_api.api.common.common_test_case import CommonTestCase
from wenet_service_api.api.ws.resource.common import WenetSource


# class TestMessageInterface(CommonTestCase):
#
#     def test_post(self):
#
#         message = {
#             "messageId": "message id",
#             "channel": "channel",
#             "userId": "user_id",
#             "appId": "app_id",
#             "type": "request",
#             "content": {
#                 "type": "textual_message",
#                 "value": "value"
#             },
#             "domain": "domain",
#             "intent": {
#                 "name": "name",
#                 "confidence": 0.9
#             },
#             "entities": [{
#                 "name": "name",
#                 "value": "value",
#                 "confidence": 0.9
#             }],
#             "language": "it",
#             "metadata": {}
#         }
#
#         response = self.client.post("/messages", json=message, headers={"apikey": self.AUTHORIZED_APIKEY, "x-wenet-source": WenetSource.COMPONENT.value})
#         self.assertEqual(response.status_code, 201)
#
#     def test_post_not_authorized(self):
#
#         message = {
#             "messageId": "message id",
#             "channel": "channel",
#             "userId": "user_id",
#             "appId": "app_id",
#             "type": "request",
#             "content": {
#                 "type": "textual_message",
#                 "value": "value"
#             },
#             "domain": "domain",
#             "intent": {
#                 "name": "name",
#                 "confidence": 0.9
#             },
#             "entities": [{
#                 "name": "name",
#                 "value": "value",
#                 "confidence": 0.9
#             }],
#             "language": "it",
#             "metadata": {}
#         }
#
#         response = self.client.post("/messages", json=message)
#         self.assertEqual(response.status_code, 401)
#
#     def test_post2(self):
#
#         message = {
#             "channel": "channel",
#             "userId": "user_id",
#             "appId": "app_id",
#             "type": "request",
#             "content": {
#                 "type": "textual_message",
#                 "value": "value"
#             },
#             "domain": "domain",
#             "intent": {
#                 "name": "name",
#                 "confidence": 0.9
#             },
#             "entities": [{
#                 "name": "name",
#                 "value": "value",
#                 "confidence": 0.9
#             }],
#             "language": "it",
#             "metadata": {}
#         }
#
#         response = self.client.post("/messages", json=message, headers={"apikey": self.AUTHORIZED_APIKEY, "x-wenet-source": WenetSource.COMPONENT.value})
#         self.assertEqual(response.status_code, 400)

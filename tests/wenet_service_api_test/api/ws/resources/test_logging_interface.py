from __future__ import absolute_import, annotations

import json
from datetime import datetime

from mock import Mock

from tests.wenet_service_api_test.api.common.common_test_case import CommonTestCase
from wenet.common.model.app.app_dto import App, AppStatus
from wenet.common.model.logging_messages.contents import ActionContent
from wenet.common.model.logging_messages.messages import RequestMessage
from wenet.common.model.scope import Scope
from wenet_service_api.api.ws.resource.common import WenetSource
from wenet_service_api.common.exception.exceptions import BadRequestException


class TestLoggingInterface(CommonTestCase):
    app = App(
        app_id="1",
        status=AppStatus.ACTIVE,
        message_callback_url="url",
        metadata={},
        creation_ts=int(datetime(2020, 2, 27).timestamp()),
        last_update_ts=int(datetime(2020, 2, 27).timestamp())
    )

    developer_lis = ["1"]
    user_list = ["1", "11"]

    def test_post_message(self):
        message = RequestMessage(
            message_id="message_id",
            channel="channel",
            user_id="user_id",
            project="project",
            content=ActionContent(
                button_text="text",
                button_payload="payload"
            ),
            timestamp=datetime.now()
        )

        self.service_collector_connector.logger_connector.post_messages = Mock(return_value=["message_id"])
        response = self.client.post("/log/messages", json=message.to_repr(), headers={"apikey": self.AUTHORIZED_APIKEY, "x-wenet-source": WenetSource.COMPONENT.value})

        self.assertEqual(201, response.status_code)
        self.service_collector_connector.logger_connector.post_messages.assert_called_once()

    def test_post_messages(self):
        messages = [
            RequestMessage(
                message_id="message_id",
                channel="channel",
                user_id="user_id",
                project="project",
                content=ActionContent(
                    button_text="text",
                    button_payload="payload"
                ),
                timestamp=datetime.now()
            ),
            RequestMessage(
                message_id="message_id2",
                channel="channel",
                user_id="user_id",
                project="project",
                content=ActionContent(
                    button_text="text",
                    button_payload="payload"
                ),
                timestamp=datetime.now()
            )
        ]

        json_messages = [x.to_repr() for x in messages]

        self.service_collector_connector.logger_connector.post_messages = Mock(return_value=["message_id", "message_id2"])
        response = self.client.post("/log/messages", json=json_messages, headers={"apikey": self.AUTHORIZED_APIKEY, "x-wenet-source": WenetSource.COMPONENT.value})

        self.assertEqual(201, response.status_code)
        self.service_collector_connector.logger_connector.post_messages.assert_called_once()

    def test_post_bad_request(self):
        messages = [
            RequestMessage(
                message_id="message_id",
                channel="channel",
                user_id="user_id",
                project="project",
                content=ActionContent(
                    button_text="text",
                    button_payload="payload"
                ),
                timestamp=datetime.now()
            ),
            RequestMessage(
                message_id="message_id2",
                channel="channel",
                user_id="user_id",
                project="project",
                content=ActionContent(
                    button_text="text",
                    button_payload="payload"
                ),
                timestamp=datetime.now()
            )
        ]

        json_messages = [x.to_repr() for x in messages]

        self.service_collector_connector.logger_connector.post_messages = Mock(side_effect=BadRequestException)
        response = self.client.post("/log/messages", json=json_messages, headers={"apikey": self.AUTHORIZED_APIKEY, "x-wenet-source": WenetSource.COMPONENT.value})

        self.assertEqual(400, response.status_code)
        self.service_collector_connector.logger_connector.post_messages.assert_called_once()

        json_response = json.loads(response.data)

        self.assertNotIsInstance(json_response, list)

    def test_post_messages_oauth(self):
        messages = [
            RequestMessage(
                message_id="message_id",
                channel="channel",
                user_id="user_id",
                project="project",
                content=ActionContent(
                    button_text="text",
                    button_payload="payload"
                ),
                timestamp=datetime.now()
            ),
            RequestMessage(
                message_id="message_id2",
                channel="channel",
                user_id="user_id",
                project="project",
                content=ActionContent(
                    button_text="text",
                    button_payload="payload"
                ),
                timestamp=datetime.now()
            )
        ]

        json_messages = [x.to_repr() for x in messages]

        self.service_collector_connector.hub_connector.get_app = Mock(return_value=self.app)
        self.service_collector_connector.hub_connector.get_app_users = Mock(return_value=self.user_list)

        self.service_collector_connector.logger_connector.post_messages = Mock(return_value=["message_id", "message_id2"])
        response = self.client.post("/log/messages", json=json_messages, headers={
            "apikey": self.AUTHORIZED_APIKEY,
            "x-wenet-source": WenetSource.OAUTH2_AUTHORIZATION_CODE.value,
            "X-Authenticated-Scope": f"{Scope.CONVERSATIONS.value} {Scope.FIRST_NAME.value}",
            "X-Authenticated-Userid": "user_id",
            "X-Consumer-Username": "app_1"
        })

        self.assertEqual(201, response.status_code)
        self.service_collector_connector.logger_connector.post_messages.assert_called_once()

        json_response = json.loads(response.data)

        self.assertFalse("warning" in json_response)

    def test_post_messages_oauth_multiple_users(self):
        messages = [
            RequestMessage(
                message_id="message_id",
                channel="channel",
                user_id="user_id",
                project="project",
                content=ActionContent(
                    button_text="text",
                    button_payload="payload"
                ),
                timestamp=datetime.now()
            ),
            RequestMessage(
                message_id="message_id2",
                channel="channel",
                user_id="user_id1",
                project="project",
                content=ActionContent(
                    button_text="text",
                    button_payload="payload"
                ),
                timestamp=datetime.now()
            )
        ]

        json_messages = [x.to_repr() for x in messages]

        self.service_collector_connector.hub_connector.get_app = Mock(return_value=self.app)
        self.service_collector_connector.hub_connector.get_app_users = Mock(return_value=self.user_list)

        self.service_collector_connector.logger_connector.post_messages = Mock(return_value=["message_id", "message_id2"])
        response = self.client.post("/log/messages", json=json_messages, headers={
            "apikey": self.AUTHORIZED_APIKEY,
            "x-wenet-source": WenetSource.OAUTH2_AUTHORIZATION_CODE.value,
            "X-Authenticated-Scope": f"{Scope.CONVERSATIONS.value} {Scope.FIRST_NAME.value}",
            "X-Authenticated-Userid": "user_id",
            "X-Consumer-Username": "app_1"
        })

        self.assertEqual(201, response.status_code)
        self.service_collector_connector.logger_connector.post_messages.assert_called_once()

        json_response = json.loads(response.data)

        self.assertTrue("warning" in json_response)

    def test_post_messages_oauth_not_authorized(self):
        messages = [
            RequestMessage(
                message_id="message_id",
                channel="channel",
                user_id="user_id",
                project="project",
                content=ActionContent(
                    button_text="text",
                    button_payload="payload"
                ),
                timestamp=datetime.now()
            ),
            RequestMessage(
                message_id="message_id2",
                channel="channel",
                user_id="user_id",
                project="project",
                content=ActionContent(
                    button_text="text",
                    button_payload="payload"
                ),
                timestamp=datetime.now()
            )
        ]

        json_messages = [x.to_repr() for x in messages]

        self.service_collector_connector.hub_connector.get_app = Mock(return_value=self.app)
        self.service_collector_connector.hub_connector.get_app_users = Mock(return_value=self.user_list)

        self.service_collector_connector.logger_connector.post_messages = Mock(return_value=["message_id", "message_id2"])
        response = self.client.post("/log/messages", json=json_messages, headers={
            "apikey": self.AUTHORIZED_APIKEY,
            "x-wenet-source": WenetSource.OAUTH2_AUTHORIZATION_CODE.value,
            "X-Authenticated-Scope": f"{Scope.FIRST_NAME.value}",
            "X-Authenticated-Userid": "11",
            "X-Consumer-Username": "app_1"
        })

        self.assertEqual(401, response.status_code)
        self.service_collector_connector.logger_connector.post_messages.assert_not_called()

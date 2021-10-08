from __future__ import absolute_import, annotations

import logging

from flask import request
from flask_restful import abort
from wenet.interface.exceptions import AuthenticationException

from wenet.model.logging_message.message import BaseMessage
from wenet.model.scope import Scope
from wenet_service_api.api.ws.resource.common import AuthenticatedResource, WenetSource, AuthenticationResult, \
    ComponentAuthentication, Oauth2Result
from wenet_service_api.connector.collector import ServiceConnectorCollector

logger = logging.getLogger("api.api.ws.resource.logging")


class MessageLoggingInterfaceBuilder:

    @staticmethod
    def routes(service_connector_collector: ServiceConnectorCollector, authorized_apikey: str):
        return [
            (MessageLoggingInterface, "/messages", (service_connector_collector, authorized_apikey))
        ]


class MessageLoggingInterface(AuthenticatedResource):

    def __init__(self, service_connector_collector: ServiceConnectorCollector, authorized_apikey: str) -> None:
        super().__init__(authorized_apikey, service_connector_collector)

    @staticmethod
    def _can_log(authentication_result: AuthenticationResult) -> bool:
        """
        check if the caller is properly authenticated
        @param authentication_result:
        @return:
        """
        if isinstance(authentication_result, ComponentAuthentication):
            return True
        elif isinstance(authentication_result, Oauth2Result):
            return Scope.CONVERSATIONS in authentication_result.scopes
        else:
            return False

    @staticmethod
    def _can_log_message(message: BaseMessage, authentication_result: AuthenticationResult):
        """
        Check if an the caller can og a specific message
        @param message:
        @param authentication_result:
        """
        if isinstance(authentication_result, ComponentAuthentication):
            return True
        elif isinstance(authentication_result, Oauth2Result):
            return message.user_id == authentication_result.wenet_user_id or message.user_id == authentication_result.app.app_id
        else:
            return False

    def post(self):

        authentication_result = self._check_authentication([WenetSource.COMPONENT, WenetSource.OAUTH2_AUTHORIZATION_CODE])

        if not self._can_log(authentication_result):
            if isinstance(authentication_result, Oauth2Result):
                logger.info(f"Missing conversation scope, unable to log the message for the user [{authentication_result.wenet_user_id}] and app [{authentication_result.app}]")
                message = "the conversation scope is required  to save the logs"
            else:
                message = "The conversation logging is not allowed with this authentication method"
            abort(401, message=message)
            return

        try:
            posted_data: dict = request.get_json()
        except Exception as e:
            logger.exception("Invalid body message", exc_info=e)
            abort(400, message="Invalid JSON - Unable to parse message body")
            return

        if isinstance(posted_data, list):
            try:
                messages = [BaseMessage.from_repr(x) for x in posted_data]
            except (ValueError, TypeError, KeyError) as v:
                logger.exception(f"Unable to build a list of messages from payload [{posted_data}]")
                abort(400, message="Malformed message")
                return
        else:
            try:
                messages = [BaseMessage.from_repr(posted_data)]
            except (ValueError, TypeError, KeyError) as v:
                logger.exception(f"Unable to build a BaseMessage from [{posted_data}]", exc_info=v)
                abort(400, message="Malformed message")
                return

        ok_messages = []
        wrong_messages = []

        for message in messages:
            if self._can_log_message(message, authentication_result):
                ok_messages.append(message)
            else:
                wrong_messages.append(message)

        try:
            self._service_connector_collector.logger_connector.post_messages(ok_messages)
            logger.info(f"Received new LogMessages to save [{messages}]")

            if not wrong_messages:
                return {}, 201
            else:
                return {
                    "warning": "Some of the messages has not been saved due to some scope problems"
                }, 201
        except AuthenticationException as e:
            logger.exception(f"Unauthorized to post messages", exc_info=e)
            abort(403)
            return
        # except BadRequestException as e:
        #     logger.exception(f"Bad request during message logging of the messages [{messages}]", exc_info=e)
        #     abort(400, messages="Bad request")
        #     return
        except Exception as e:
            logger.exception("Unable to store the messages", exc_info=e)
            abort(500)
            return

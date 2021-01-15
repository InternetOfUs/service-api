from __future__ import absolute_import, annotations

import logging

from flask import request
from flask_restful import abort

from wenet.common.model.logging_messages.messages import BaseMessage
from wenet_service_api.api.ws.resource.common import AuthenticatedResource, WenetSource
from wenet_service_api.common.exception.exceptions import BadRequestException
from wenet_service_api.connector.collector import ServiceConnectorCollector

logger = logging.getLogger("api.api.ws.resource.logging")


class MessageLoggingInterface(AuthenticatedResource):

    def __init__(self, service_connector_collector: ServiceConnectorCollector, authorized_apikey: str) -> None:
        super().__init__(authorized_apikey, service_connector_collector)

    def post(self):

        self._check_authentication([WenetSource.COMPONENT, WenetSource.OAUTH2_AUTHORIZATION_CODE])

        try:
            posted_data: dict = request.get_json()
        except Exception as e:
            logger.exception("Invalid body message", exc_info=e)
            abort(400, message="Invalid JSON - Unable to parse message body")
            return

        if isinstance(posted_data, list):
            try:
                messages = [BaseMessage.from_repr(x) for x in posted_data]
            except (ValueError, TypeError) as v:
                logger.exception(f"Unable to build a list of messages from payload [{posted_data}]")
                abort(400, message="Malformed message")
                return
        else:
            try:
                messages = [BaseMessage.from_repr(posted_data)]
            except (ValueError, TypeError) as v:
                logger.exception(f"Unable to build a BaseMessage from [{posted_data}]", exc_info=v)
                abort(400, message="Malformed message")
                return

        try:
            traces = self._service_connector_collector.logger_connector.post_messages(messages)
            logger.info(f"Received new LogMessages to save [{messages}]")
            return traces, 201
        except BadRequestException as e:
            logger.exception(f"Bad request during message logging of the messages [{messages}]", exc_info=e)
            abort(400, messages="Bad request")
            return
        except Exception as e:
            logger.exception("Unable to store the messages", exc_info=e)
            abort(500)
            return

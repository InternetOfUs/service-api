from __future__ import absolute_import, annotations

import logging

from flask import request
from flask_restful import abort

from wenet.model.message import Message
from wenet.wenet_service_api.ws.resource.common import AuthenticatedResource

logger = logging.getLogger("wenet.wenet_service_api.ws.resource.message")


class MessageInterfaceBuilder:

    @staticmethod
    def routes(authorized_apikey: str):
        return [
            (MessageInterface, "", (authorized_apikey, ))
        ]


class MessageInterface(AuthenticatedResource):

    def __init__(self, authorized_apikey: str):
        super().__init__(authorized_apikey)

    def post(self):

        self._check_authentication()

        try:
            posted_data: dict = request.get_json()
        except Exception as e:
            logger.exception("Invalid message body", exc_info=e)
            abort(400, message="Invalid JSON - Unable to parse message body")
            return

        try:
            message = Message.from_repr(posted_data)
        except (ValueError, TypeError) as v:
            logger.exception(f"Unable to build a Message from [{posted_data}]", exc_info=v)
            abort(400, message="Some fields contains invalid parameters")
            return
        except KeyError as k:
            logger.exception(f"Unable to build a Message from [{posted_data}]", exc_info=k)
            abort(400, message=f"The field [{k}] is missing")
            return

        logger.info(f"Received nee message {message.to_repr()}")

        return {}, 201

from __future__ import absolute_import, annotations

import secrets
import uuid
from datetime import datetime

import pytz
from flask import request
from flask_restful import Resource, abort

import logging

from wenet.model.App import App

logger = logging.getLogger("wenet.wenet_service_api.ws.resource.app")


class AppResourceInterfaceBuilder:

    @staticmethod
    def routes():
        return [
            (AppPostResourceInterface, "", ()),
            (AppResourceInterface, "/<string:app_id>", ())
        ]


class AppPostResourceInterface(Resource):

    def post(self):

        try:
            posted_data: dict = request.get_json()
        except Exception as e:
            logger.exception("Invalid message body", exc_info=e)
            abort(400, message="Invalid JSON - Unable to parse message body")
            return

        if "name" not in posted_data:
            logger.warning(f"Missing name field in [{posted_data}]")
            abort(400, message=f"Missing name field in [{posted_data}]")
            return

        app_name = posted_data["name"]
        now = datetime.now(pytz.utc)

        app = App(
            app_id=str(uuid.uuid4()),
            app_token=secrets.token_urlsafe(),
            name=app_name,
            creation_ts=now,
            last_update_ts=now
        )

        logger.info(f"Created new app [{app}]")
        return app.to_repr(), 201


class AppResourceInterface(Resource):

    def get(self, app_id: str):

        app = App(
            app_id=app_id,
            app_token="fHTj98iRx_NEcTDmnVDDK_wKcLsw6vH-Y9OmqRGUu94",
            name="WeNet scenario app",
            creation_ts=datetime(2020, 2, 24, tzinfo=pytz.utc),
            last_update_ts=datetime.now(pytz.utc)
        )

        logger.info(f"Retrieved app [{app}]")
        return app.to_repr(), 200

    def put(self, app_id: str):
        try:
            posted_data: dict = request.get_json()
        except Exception as e:
            logger.exception("Invalid message body", exc_info=e)
            abort(400, message="Invalid JSON - Unable to parse message body")
            return

        try:
            app = App.from_repr(posted_data, app_id)
        except (ValueError, TypeError) as v:
            logger.exception(f"Unable to build an App from [{posted_data}]", exc_info=v)
            abort(400, message="Some fields contains invalid parameters")
            return
        except KeyError as k:
            logger.exception(f"Unable to build an App from [{posted_data}]", exc_info=k)
            abort(400, message=f"The field [{k}] is missing")
            return

        logger.info(f"Updated app [{app}]")
        return app.to_repr(), 200

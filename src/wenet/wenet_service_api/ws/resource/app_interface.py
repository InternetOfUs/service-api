from __future__ import absolute_import, annotations

import secrets
import uuid
from datetime import datetime

import pytz
from flask import request
from flask_restful import Resource, abort

import logging

from wenet.common.exception.exceptions import ResourceNotFound
from wenet.dao.dao_collector import DaoCollector
from wenet.model.app import App

logger = logging.getLogger("wenet.wenet_service_api.ws.resource.app")


class AppResourceInterfaceBuilder:

    @staticmethod
    def routes(dao_collector: DaoCollector):
        return [
            (AppPostResourceInterface, "", (dao_collector,)),
            (AppResourceInterface, "/<string:app_id>", (dao_collector,))
        ]


class AppPostResourceInterface(Resource):

    def __init__(self, dao_collector: DaoCollector) -> None:
        super().__init__()
        self._dao_collector = dao_collector

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

        try:
            self._dao_collector.app_dao.create_or_update(app)
        except Exception as e:
            logger.exception(f"Unable to save the app [{app}]", exc_info=e)
            abort(500, message="Unable to save the new application")
            return

        logger.info(f"Created new app [{app}]")
        return app.to_repr(), 201


class AppResourceInterface(Resource):

    def __init__(self, dao_collector: DaoCollector) -> None:
        super().__init__()
        self._dao_collector = dao_collector

    def get(self, app_id: str):

        try:
            app = self._dao_collector.app_dao.get(app_id)
        except ResourceNotFound:
            logger.info(f"Resource with id [{app_id}] not found")
            abort(404, message=f"Resource with id [{app_id}] not found")
            return
        except Exception as e:
            logger.exception(f"Unable to retrieve the resource with id [{app_id}]", exc_info=e)
            abort(500, message=f"Unable to retrieve the resource with id [{app_id}]")
            return

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

        try:
            stored_app = self._dao_collector.app_dao.get(app_id)
            stored_app.name = app.name
            stored_app.app_token = app.app_token
            stored_app.last_update_ts = datetime.now(pytz.utc)
            self._dao_collector.app_dao.create_or_update(stored_app)
        except ResourceNotFound:
            logger.info(f"Resource [{app_id}] not found in update operation")
            abort(404, message=f"Resource [{app_id}] not found")
        except Exception as e:
            logger.exception(f"Unable to update resource [{app_id}]", exc_info=e)
            abort(500, message=f"Unable to update resource [{app_id}]")
            return

        logger.info(f"Updated app [{app}]")
        return app.to_repr(), 200
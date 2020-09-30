from __future__ import absolute_import, annotations

from flask_restful import abort

import logging

from wenet_service_api.common.exception.exceptions import ResourceNotFound
from wenet_service_api.dao.dao_collector import DaoCollector
from wenet_service_api.api.ws.resource.common import AuthenticatedResource, WenetSource

logger = logging.getLogger("api.api.ws.resource.app")

# TODO remove
class AppResourceInterfaceBuilder:

    @staticmethod
    def routes(dao_collector: DaoCollector, authorized_apikey: str):
        return [
            (AppResourceInterface, "/<string:app_id>", (dao_collector, authorized_apikey)),
            (ListAppUserInterface, "/<string:app_id>/users", (dao_collector, authorized_apikey))
        ]


class AppResourceInterface(AuthenticatedResource):

    def __init__(self, dao_collector: DaoCollector, authorized_apikey: str) -> None:
        super().__init__(authorized_apikey, dao_collector)

    def get(self, app_id: str):

        self._check_authentication([WenetSource.COMPONENT])

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

        app_dto = app.to_app_dto()
        logger.info(f"Retrieved app [{app_dto}]")
        return app_dto.to_repr(), 200


class ListAppUserInterface(AuthenticatedResource):

    def __init__(self, dao_collector: DaoCollector, authorized_apikey: str) -> None:
        super().__init__(authorized_apikey, dao_collector)

    def get(self, app_id: str):

        self._check_authentication([WenetSource.COMPONENT])

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

        try:
            users = self._dao_collector.user_account_telegram_dao.list(app.app_id)
        except Exception as e:
            logger.exception(f"Unable to retrieve the list of account for app {app_id}", exc_info=e)
            abort(500, message=f"Unable to retrieve the list of account for app {app_id}")
            return

        id_set = set()

        for user in users:
            id_set.add(str(user.user_id))

        return list(x for x in id_set), 200

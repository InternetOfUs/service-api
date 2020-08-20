from __future__ import absolute_import, annotations

import logging

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from wenet_service_api.model.app import AppDeveloper

logger = logging.getLogger("api.api.app_developers_dao")


class AppDeveloperDao:

    def __init__(self, engine: Engine):
        self._engine = engine

    def _get_session(self) -> Session:
        session = sessionmaker(bind=self._engine)
        return session()

    def create_or_update(self, app_developer: AppDeveloper):
        session = self._get_session()
        session.merge(app_developer)
        session.commit()
        session.flush()
        session.close()

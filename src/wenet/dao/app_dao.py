from __future__ import absolute_import, annotations

import logging

from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session, joinedload

from wenet.common.exception.exceptions import ResourceNotFound
from wenet.model.app import App

logger = logging.getLogger("wenet.wenet_service_api.app_dao")


class AppDao:

    def __init__(self, engine: Engine):
        self._engine = engine

    def _get_session(self) -> Session:
        session = sessionmaker(bind=self._engine)
        return session()

    def get(self, app_id: str) -> App:
        session = self._get_session()
        result: App = session.query(App).options(joinedload(App.platform_telegram)).filter_by(app_id=app_id).first()

        session.close()

        if result is None:
            raise ResourceNotFound(f"Unable to find the app with id [{app_id}]")

        result.load_metadata_from_metadata_str()

        return result

    def create_or_update(self, app: App):
        # TODO update creation and update
        session = self._get_session()
        session.merge(app)
        session.commit()
        session.flush()
        session.close()

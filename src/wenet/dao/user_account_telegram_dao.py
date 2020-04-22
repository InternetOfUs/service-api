from __future__ import absolute_import, annotations

import logging

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker, joinedload

from wenet.common.exception.exceptions import ResourceNotFound
from wenet.model.app import UserAccountTelegram

logger = logging.getLogger("wenet.wenet_service_api.user_Account_telegram_dao")


class UserAccountTelegramDao:

    def __init__(self, engine: Engine):
        self._engine = engine

    def _get_session(self) -> Session:
        session = sessionmaker(bind=self._engine)
        return session()

    def get(self, app_id: str, telegram_id: int) -> UserAccountTelegram:
        session = self._get_session()
        result: UserAccountTelegram = session\
            .query(UserAccountTelegram)\
            .options(joinedload(UserAccountTelegram.app))\
            .filter_by(telegram_id=telegram_id, app_id=app_id)\
            .first()

        session.close()

        if result is None:
            raise ResourceNotFound(f"Unable to find an user with telegram_id [{telegram_id}] in the app [{app_id}]")

        result.load_metadata_from_metadata_str()

        return result

    def create_or_update(self, user_account_telegram: UserAccountTelegram):
        session = self._get_session()
        session.merge(user_account_telegram)
        session.commit()
        session.flush()
        session.close()

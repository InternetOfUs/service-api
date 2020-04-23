from __future__ import absolute_import, annotations

import logging
from datetime import datetime
from typing import List

import pytz
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
            .filter_by(telegram_id=telegram_id, app_id=app_id, active=1)\
            .first()

        session.close()

        if result is None:
            raise ResourceNotFound(f"Unable to find an user with telegram_id [{telegram_id}] in the app [{app_id}]")

        result.load_metadata_from_metadata_str()

        return result

    def list(self, app_id: str, user_id: str):
        session = self._get_session()

        results: List[UserAccountTelegram] = session\
            .query(UserAccountTelegram)\
            .options(joinedload(UserAccountTelegram.app))\
            .filter_by(app_id=app_id, user_id=user_id, active=1)\
            .all()

        session.close()

        for result in results:
            result.load_metadata_from_metadata_str()

        return results

    def create_or_update(self, user_account_telegram: UserAccountTelegram):
        user_account_telegram.load_metadata_str_from_metadata()
        user_account_telegram.last_update_ts = int(datetime.now(pytz.utc).timestamp())
        session = self._get_session()
        session.merge(user_account_telegram)
        session.commit()
        session.flush()
        session.close()

from __future__ import absolute_import, annotations

import sqlalchemy as db

import os

from wenet.dao.app_dao import AppDao
from wenet.dao.user_account_telegram_dao import UserAccountTelegramDao


class DaoCollector:

    def __init__(self, app_dao: AppDao, user_account_telegram_dao: UserAccountTelegramDao):
        self.app_dao = app_dao
        self.user_account_telegram_dao = user_account_telegram_dao

    @staticmethod
    def build_from_env() -> DaoCollector:
        db_connection_string = os.getenv("DB_CONNECTION_STRING")

        if db_connection_string is None:
            raise RuntimeError("Missing enviromental variable [DB_CONNECTION_STRING]")

        engine = db.create_engine(db_connection_string)
        return DaoCollector(
            app_dao=AppDao(engine),
            user_account_telegram_dao=UserAccountTelegramDao(engine)
        )

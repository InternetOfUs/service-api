from __future__ import absolute_import, annotations

import sqlalchemy as db

import os

from wenet_service_api.dao.app_dao import AppDao
from wenet_service_api.dao.app_developer_dao import AppDeveloperDao
from wenet_service_api.dao.user_account_telegram_dao import UserAccountTelegramDao


class DaoCollector:

    def __init__(self, app_dao: AppDao, user_account_telegram_dao: UserAccountTelegramDao, app_developer_dao: AppDeveloperDao):
        self.app_dao = app_dao
        self.user_account_telegram_dao = user_account_telegram_dao
        self.app_developer_dao = app_developer_dao

    @staticmethod
    def build_from_env() -> DaoCollector:

        mysql_db = os.getenv("MYSQL_DATABASE")
        mysql_user = os.getenv("MYSQL_USER")
        mysql_pass = os.getenv("MYSQL_PASSWORD")
        mysql_host = os.getenv("MYSQL_HOST")
        mysql_port = os.getenv("MYSQL_PORT")

        if mysql_db is None:
            raise RuntimeError("Missing enviromental variable [MYSQL_DATABASE]")
        if mysql_user is None:
            raise RuntimeError("Missing enviromental variable [MYSQL_USER]")
        if mysql_pass is None:
            raise RuntimeError("Missing enviromental variable [MYSQL_PASSWORD]")
        if mysql_host is None:
            raise RuntimeError("Missing enviromental variable [MYSQL_HOST]")
        if mysql_port is None:
            raise RuntimeError("Missing enviromental variable [MYSQL_PORT]")

        db_connection_string = f"mysql+mysqlconnector://{mysql_user}:{mysql_pass}@{mysql_host}:{mysql_port}/{mysql_db}"

        engine = db.create_engine(db_connection_string, pool_size=5, pool_recycle=3600, pool_pre_ping=True)
        return DaoCollector(
            app_dao=AppDao(engine),
            user_account_telegram_dao=UserAccountTelegramDao(engine),
            app_developer_dao=AppDeveloperDao(engine)
        )

from __future__ import absolute_import, annotations

from sqlalchemy import MetaData, Table, Column, String, create_engine, DateTime, Integer, Text, ForeignKey
from sqlalchemy.orm import relation

from wenet.dao.app_dao import AppDao
from wenet.dao.dao_collector import DaoCollector
from wenet.dao.user_account_telegram_dao import UserAccountTelegramDao


class DataAccessLayer:
    connection = None
    engine = None
    conn_string = None
    meta = MetaData()
    application = Table(
        "app", meta,
        Column("id", String(128), primary_key=True),
        Column("status", Integer, nullable=False),
        Column("name", String(512), nullable=False),
        Column("description", Text, nullable=True),
        Column("token", String(512), nullable=False),
        Column("message_callback_url", Text, nullable=True),
        Column("metadata", Text, nullable=False),
        Column("created_at", Integer),
        Column("updated_at", Integer),
    )
    platform_telegram = Table(
        "app_platform_telegram", meta,
        Column("id", Integer, primary_key=True),
        Column("app_id", String(128), ForeignKey("app.id")),
        Column("bot_username", String(128)),
        Column("updated_at", Integer),
        Column("created_at", Integer)
    )
    user_account_telegram = Table(
        "user_account_telegram", meta,
        Column("id", Integer, primary_key=True),
        Column("app_id", ForeignKey("app.id")),
        Column("user_id", Integer),
        Column("telegram_id", Integer),
        Column("created_at", Integer),
        Column("updated_at", Integer),
        Column("metadata", Text),
        Column("active", Integer)

    )

    def db_init(self, conn_string):
        self.engine = create_engine(conn_string or self.conn_string)
        self.meta.create_all(self.engine)
        self.connection = self.engine.connect()


class MockDaoCollector(DaoCollector):

    @staticmethod
    def build_from_env() -> DaoCollector:
        dal = DataAccessLayer()
        dal.db_init("sqlite:///:memory:")
        return DaoCollector(
            app_dao=AppDao(dal.engine),
            user_account_telegram_dao=UserAccountTelegramDao(dal.engine)
        )

from __future__ import absolute_import, annotations

from sqlalchemy import MetaData, Table, Column, String, create_engine, DateTime

from wenet.dao.app_dao import AppDao
from wenet.dao.dao_collector import DaoCollector


class DataAccessLayer:
    connection = None
    engine = None
    conn_string = None
    meta = MetaData()
    application = Table(
        "app", meta,
        Column("app_id", String, primary_key=True),
        Column("app_token", String(256)),
        Column("name", String(256)),
        Column("creation_ts", DateTime),
        Column("last_update_ts", DateTime)
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
            app_dao=AppDao(dal.engine)
        )

from __future__ import absolute_import, annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class App(Base):

    __tablename__ = 'app'

    app_id = Column("app_id", String, primary_key=True)
    app_token = Column("app_token", String(256))
    name = Column("name", String(256))
    creation_ts = Column("creation_ts", DateTime)
    last_update_ts = Column("last_update_ts", DateTime)

    def __init__(self, app_id: str, app_token: str, name: str, creation_ts: Optional[datetime], last_update_ts: Optional[datetime]):
        self.app_id = app_id
        self.app_token = app_token
        self.name = name
        self.creation_ts = creation_ts
        self.last_update_ts = last_update_ts

        if not isinstance(self.app_id, str):
            raise TypeError("AppId should be a string")
        if not isinstance(self.app_token, str):
            raise TypeError("AppToken should be a string")
        if not isinstance(self.name, str):
            raise TypeError("Name should be a string")
        if self.creation_ts is not None:
            if not isinstance(self.creation_ts, datetime):
                raise TypeError("CreationTs should be a datetime")
        if self.last_update_ts is not None:
            if not isinstance(self.last_update_ts, datetime):
                raise TypeError("LastUpdateDatetime should be a datetime")

    def to_repr(self) -> dict:
        return {
            "creationTs": self.creation_ts.timestamp() if self.creation_ts else None,
            "lastUpdateTs": self.last_update_ts.timestamp() if self.last_update_ts else None,
            "appId": self.app_id,
            "appToken": self.app_token,
            "name": self.name
        }

    @staticmethod
    def from_repr(raw_data: dict, app_id: Optional[str] = None) -> App:

        if app_id is None:
            app_id = raw_data["appId"]

        return App(
            app_id=app_id,
            app_token=raw_data["appToken"],
            name=raw_data["name"],
            creation_ts=datetime.fromtimestamp(float(raw_data["creationTs"])) if raw_data.get("creationTs", None) is not None else None,
            last_update_ts=datetime.fromtimestamp(float(raw_data["lastUpdateTs"])) if raw_data.get("lastUpdateTs", None) is not None else None
        )

    def __eq__(self, o) -> bool:
        if not isinstance(o, App):
            return False
        return self.app_id == o.app_id and self.app_token == o.app_token and self.name == o.name and self.creation_ts == o.creation_ts and self.last_update_ts == o.last_update_ts

    def __repr__(self):
        return str(self.to_repr())

    def __str__(self):
        return self.__repr__()

from __future__ import absolute_import, annotations

import json
from datetime import datetime
from typing import Optional, List, Union

from sqlalchemy import Column, String, DateTime, Integer, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation

from wenet.model.platform_dto import PlatformDTO, TelegramPlatformDTO

Base = declarative_base()


class App(Base):

    __tablename__ = 'app'

    app_id = Column("id", String(128), primary_key=True)
    status = Column("status", Integer, nullable=False)
    name = Column("name", String(512), nullable=False)
    description = Column("description", Text, nullable=True)
    app_token = Column("token", String(512), nullable=False)
    message_call_back_url = Column("message_callback_url", Text, nullable=True)
    metadata_str = Column("metadata", Text, nullable=False)
    creation_ts = Column("created_at", Integer)
    last_update_ts = Column("updated_at", Integer)
    platform_telegram = relation("PlatformTelegram", back_populates="app", uselist=False)

    def __init__(self, app_id: str, status: str, name: str, description: Optional[str], app_token: str, message_callback_url: Optional[str], metadata: Optional[Union[str, dict]], creation_ts: Optional[int], last_update_ts: Optional[int]):
        self.app_id = app_id
        self.status = status
        self.name = name
        self.description = description
        self.app_token = app_token
        self.message_call_back_url = message_callback_url
        self.creation_ts = creation_ts
        self.last_update_ts = last_update_ts

        if metadata is not None:
            if isinstance(metadata, str):
                self.metadata_str = metadata
                self.metadata = json.loads(metadata)
            elif isinstance(metadata, dict):
                self.metadata = metadata
                self.metadata_str = json.dumps(metadata)
            else:
                raise TypeError(f"Unable to build metadata from type [{type(metadata)}]")
        else:
            self.metadata = {}
            self.metadata_str = json.dumps(self.metadata)

    def load_metadata_from_metadata_str(self):
        if self.metadata_str:
            self.metadata = json.loads(self.metadata_str)
        else:
            self.metadata = {}

    def load_metadata_str_from_metadata(self) -> None:
        if self.metadata is not None:
            self.metadata_str = json.dumps(self.metadata)


class PlatformTelegram(Base):
    __tablename__ = "app_platform_telegram"

    id = Column("id", Integer, primary_key=True)
    app_id = Column("app_id", String(128), ForeignKey("app.id"))
    bot_username = Column("bot_username", String(128))
    last_update_ts = Column("updated_at", Integer)
    creation_ts = Column("created_at", Integer)
    app = relation("App", back_populates="platform_telegram", uselist=False)


class UserAccountTelegram(Base):

    __tablename__ = "user_account_telegram"

    id = Column("id", Integer, primary_key=True)
    app_id = Column("app_id", String(128), ForeignKey("app.id"))
    user_id = Column("user_id", Integer)
    telegram_id = Column("telegram_id", Integer)
    creation_ts = Column("created_at", Integer)
    last_update_ts = Column("updated_at", Integer)
    metadata_str = Column("metadata", Text)
    active = Column("active", Integer)

    app = relation("App")

    def __init__(self, user_account_id: int, app_id: str, user_id: str, telegram_id: int, creation_ts: int, last_update_ts: int, metadata: Optional[Union[str, dict]], active: int):
        self.id = user_account_id
        self.app_id = app_id
        self.user_id = user_id
        self.telegram_id = telegram_id
        self.creation_ts = creation_ts
        self.last_update_ts = last_update_ts
        self.active = active

        if metadata:
            if isinstance(metadata, str):
                self.metadata = json.loads(metadata)
                self.metadata_str = metadata
            elif isinstance(metadata, dict):
                self.metadata = metadata
                self.metadata_str = json.dumps(metadata)
            else:
                raise TypeError(f"Unable to build metadata from type [{type(metadata)}]")
        else:
            self.metadata = {}
            self.metadata_str = json.dumps(self.metadata)

    def load_metadata_from_metadata_str(self) -> None:
        if self.metadata_str:
            self.metadata = json.loads(self.metadata_str)
        else:
            self.metadata = {}
            self.metadata_str = json.dumps(self.metadata)

    def load_metadata_str_from_metadata(self) -> None:
        if self.metadata is not None:
            self.metadata_str = json.dumps(self.metadata)


class AppDTO:

    def __init__(self, creation_ts: Optional[int], last_update_ts: Optional[int], app_id: str, app_token: str, allowed_platforms: List[PlatformDTO], message_callback_url: Optional[str], metadata: Optional[dict]):
        self.creation_ts = creation_ts
        self.last_update_ts = last_update_ts
        self.app_id = app_id
        self.app_token = app_token
        self.allowed_platforms = allowed_platforms
        self.message_callback_url = message_callback_url
        self.metadata = metadata

        if not self.metadata:
            self.metadata = {}

        if self.creation_ts is not None:
            if not isinstance(self.creation_ts, int):
                raise TypeError("creationTs should be a int")
        if self.last_update_ts is not None:
            if not isinstance(self.last_update_ts, int):
                raise TypeError("lastUpdateTs should be a int")

        if not isinstance(self.app_id, str):
            raise TypeError("App id should be a string")
        if not isinstance(self.app_token, str):
            raise TypeError("AppToken should be a string")
        if isinstance(self.allowed_platforms, list):
            for platforms in self.allowed_platforms:
                if not isinstance(platforms, PlatformDTO):
                    raise TypeError("AllowedPlatforms should be a list of Platforms")
        else:
            raise TypeError("AllowedPlatforms should be a list of Platforms")

        if not isinstance(self.metadata, dict):
            raise TypeError("metadata should be a dictionary")

    def to_repr(self) -> dict:
        return {
            "creationTs": self.creation_ts,
            "lastUpdateTs": self.last_update_ts,
            "appId": self.app_id,
            "appToken": self.app_token,
            "allowedPlatforms": list(x.to_repr() for x in self.allowed_platforms),
            "messageCallbackUrl": self.message_callback_url,
            "metadata": self.metadata
        }

    @staticmethod
    def from_repr(raw_data: dict) -> AppDTO:
        return AppDTO(
            creation_ts=raw_data.get("creationTs", None),
            last_update_ts=raw_data.get("lastUpdateTs", None),
            app_id=raw_data["appId"],
            app_token=raw_data["appToken"],
            allowed_platforms=list(PlatformDTO.from_repr(x) for x in raw_data["allowedPlatforms"]),
            message_callback_url=raw_data.get("messageCallbackUrl", None),
            metadata=raw_data.get("metadata", None)
        )

    def __eq__(self, o):
        if not isinstance(o, AppDTO):
            return False
        return self.app_id == o.app_id and self.app_token == o.app_token and self.allowed_platforms == o.allowed_platforms \
            and self.message_callback_url == o.message_callback_url and self.metadata == o.metadata

    def __repr__(self):
        return str(self.to_repr())

    def __str__(self):
        return self.__str__()

    @staticmethod
    def from_app(app: App) -> AppDTO:

        if app.platform_telegram:
            allowed_platforms = [
                TelegramPlatformDTO.from_platform_telegram(app.platform_telegram)
            ]
        else:
            allowed_platforms = []

        return AppDTO(
            creation_ts=app.creation_ts,
            last_update_ts=app.last_update_ts,
            app_id=app.app_id,
            app_token=app.app_token,
            allowed_platforms=allowed_platforms,
            message_callback_url=app.message_call_back_url,
            metadata=app.metadata
        )

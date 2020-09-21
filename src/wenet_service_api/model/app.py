from __future__ import absolute_import, annotations

import json
from typing import Optional, Union

from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation

from wenet.common.model.app.app_dto import AppDTO
from wenet.common.model.app.platform_dto import TelegramPlatformDTO
from wenet.common.model.user.authentication_account import TelegramAuthenticationAccount

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
    app_developers = relation("AppDeveloper", back_populates="app", uselist=True)

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

    def to_app_dto(self) -> AppDTO:

        return AppDTO(
            creation_ts=self.creation_ts,
            last_update_ts=self.last_update_ts,
            app_id=self.app_id,
            app_token=self.app_token,
            message_callback_url=self.message_call_back_url,
            metadata=self.metadata
        )


class AppDeveloper(Base):

    __tablename__ = "app_developer"

    app_id = Column("app_id", String(128), ForeignKey("app.id"), primary_key=True)
    user_id = Column("user_id", Integer, primary_key=True)
    created_at = Column("created_at", Integer)
    app = relation("App")

    def __init__(self, app_id: str, user_id: int, created_at: int):
        self.app_id = app_id
        self.user_id = user_id
        self.created_at = created_at


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

    def __init__(self, user_account_id: int, app_id: str, user_id: int, telegram_id: int, creation_ts: int, last_update_ts: int, metadata: Optional[Union[str, dict]], active: int):
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

    def to_telegram_authentication_account(self) -> TelegramAuthenticationAccount:
        return TelegramAuthenticationAccount(
            app_id=self.app_id,
            metadata=self.metadata,
            telegram_id=self.telegram_id,
            user_id=self.user_id
        )

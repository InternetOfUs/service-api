from __future__ import absolute_import, annotations

import abc
from typing import Optional

from wenet.model.common import PlatformType


class AuthenticationAccount(abc.ABC):

    def __init__(self, account_type: PlatformType):
        self.account_type = account_type

    def to_repr(self) -> dict:
        return {
            "type": self.account_type.value
        }

    @staticmethod
    def from_repr(raw_data: dict) -> AuthenticationAccount:
        account_type = PlatformType(raw_data["type"])

        if account_type == PlatformType.TELEGRAM:
            return TelegramAuthenticationAccount.from_repr(raw_data)
        else:
            raise ValueError(f"Unable to build a TelegramAuthenticationAccount from type [{account_type.value}]")

    def __eq__(self, o):
        if not isinstance(o, AuthenticationAccount):
            return False
        return self.account_type == o.account_type

    def __repr__(self) -> str:
        return str(self.to_repr())

    def __str__(self) -> str:
        return self.__repr__()


class TelegramAuthenticationAccount(AuthenticationAccount):

    def __init__(self, app_id: str, metadata: Optional[dict], telegram_id: int):
        super().__init__(PlatformType.TELEGRAM)
        self.app_id = app_id
        self.metadata = metadata
        self.telegram_id = telegram_id

        if not isinstance(app_id, str):
            raise TypeError("app_id should be a string")

        if metadata:
            if not isinstance(metadata, dict):
                raise TypeError("metadata should be a dictionary")
        else:
            self.metadata = {}

        if not isinstance(telegram_id, int):
            raise TypeError("telegram_id should be an integer")

    def to_repr(self) -> dict:
        return {
            "type": self.account_type.value,
            "appId": self.app_id,
            "metadata": self.metadata,
            "telegramId": self.telegram_id
        }

    @staticmethod
    def from_repr(raw_data: dict) -> TelegramAuthenticationAccount:
        return TelegramAuthenticationAccount(
            app_id=raw_data["appId"],
            metadata=raw_data.get("metadata", None),
            telegram_id=raw_data["telegramId"]
        )

    def __eq__(self, o):
        if not isinstance(o, TelegramAuthenticationAccount):
            return False
        return self.app_id == o.app_id and self.metadata == o.metadata and self.telegram_id == o.telegram_id

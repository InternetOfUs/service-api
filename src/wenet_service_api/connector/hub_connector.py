from __future__ import absolute_import, annotations

import logging
import os
from datetime import datetime
from typing import List, Optional

import requests

from wenet.common.model.app.app_dto import AppDeveloper, AppStatus, App
from wenet_service_api.common.exception.exceptions import ResourceNotFound
from wenet_service_api.connector.service_connector import ServiceConnector

logger = logging.getLogger("api.connector.hub")


class HubConnector(ServiceConnector):

    @staticmethod
    def build_from_env(extra_headers: Optional[dict] = None) -> HubConnector:

        base_url = os.getenv("HUB_CONNECTOR_BASE_URL")

        if not base_url:
            raise RuntimeError("ENV: HUB_CONNECTOR_BASE_URL is not defined")

        base_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        if extra_headers is not None:
            base_headers.update(extra_headers)

        return HubConnector(
            base_url=base_url,
            base_headers=base_headers
        )

    def get_app(self, app_id: str, headers: Optional[dict] = None) -> App:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        url = f"{self._base_url}/data/app/{app_id}"

        response = requests.get(url, headers)

        if response.status_code == 200:
            return App.from_repr(response.json())
        elif response.status_code == 404:
            raise ResourceNotFound()
        else:
            raise Exception(f"Unable to retrieve the application, server responds with {response.status_code}")

    def get_app_developers(self, app_id: str, headers: Optional[dict] = None) -> List[str]:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = requests.get(f"{self._base_url}/data/app/{app_id}/developer", headers)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            raise ResourceNotFound()
        else:
            raise Exception(f"Unable to retrieve the application, server responds with {response.status_code}")

    def get_app_users(self, app_id: str, headers: Optional[dict] = None) -> List[str]:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = requests.get(f"{self._base_url}/data/app/{app_id}/user", headers)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            raise ResourceNotFound()
        else:
            raise Exception(f"Unable to retrieve the application, server responds with {response.status_code}")


class DummyHubConnector(HubConnector):

    def __init__(self):
        super().__init__("", None)

    @staticmethod
    def build_from_env(extra_headers: Optional[dict] = None) -> HubConnector:
        return DummyHubConnector()

    def get_app(self, app_id: str, headers: Optional[dict] = None) -> App:
        return App(
            creation_ts=datetime.now().timestamp(),
            last_update_ts=datetime.now().timestamp(),
            app_id="1",
            status=AppStatus.ACTIVE,
            message_callback_url=None,
            metadata=None
        )

    def get_app_developers(self, app_id: str, headers: Optional[dict] = None) -> List[AppDeveloper]:
        return [
            AppDeveloper(
                "1",
                "2"
            ),
            AppDeveloper(
                "1",
                "2"
            )
        ]

    def get_app_users(self, app_id: str, headers: Optional[dict] = None) -> List[str]:
        return [
            "1",
            "2",
            "3",
            "4"
        ]

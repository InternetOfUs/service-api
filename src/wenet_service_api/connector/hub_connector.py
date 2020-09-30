from __future__ import absolute_import, annotations

import logging
import os
from datetime import datetime
from typing import List, Optional

import requests

from wenet.common.model.app.app_dto import AppDTO, AppDeveloper, AppStatus
from wenet_service_api.common.exception.exceptions import ResourceNotFound
from wenet_service_api.connector.service_connector import ServiceConnector

logger = logging.getLogger("api.connector.hub")


class HubConnector(ServiceConnector):

    @staticmethod
    def build_from_env() -> HubConnector:

        base_url = os.getenv("HUB_CONNECTOR_BASE_URL")

        if not base_url:
            raise RuntimeError("ENV: HUB_CONNECTOR_BASE_URL is not defined")

        return HubConnector(
            base_url=base_url,
            base_headers={
                "Accept": "application/json",
                "Content-Type": "application/json"
                # TODO auth
            }
        )

    def get_app(self, app_id: str, headers: Optional[dict] = None) -> AppDTO:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = requests.get(f"{self._base_url}/app/{app_id}", headers)

        if response.status_code == 200:
            return AppDTO.from_repr(response.json())
        elif response.status_code == 404:
            raise ResourceNotFound()
        else:
            raise Exception(f"Unable to retrieve the application, server responds with {response.status_code}")

    def get_app_developers(self, app_id: str, headers: Optional[dict] = None) -> List[AppDeveloper]:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = requests.get(f"{self._base_url}/app/{app_id}/developers", headers)

        if response.status_code == 200:
            return [AppDeveloper.from_repr(x) for x in response.json()]
        elif response.status_code == 404:
            raise ResourceNotFound()
        else:
            raise Exception(f"Unable to retrieve the application, server responds with {response.status_code}")


class DummyHubConnector(HubConnector):

    def __init__(self):
        super().__init__("", None)

    @staticmethod
    def build_from_env() -> HubConnector:
        return DummyHubConnector()

    def get_app(self, app_id: str, headers: Optional[dict] = None) -> AppDTO:
        return AppDTO(
            creation_ts=datetime.now().timestamp(),
            last_update_ts=datetime.now().timestamp(),
            app_id="1",
            app_token=None,
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

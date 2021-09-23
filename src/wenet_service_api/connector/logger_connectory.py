from __future__ import absolute_import, annotations

from typing import Optional, List

import requests
import os
import logging

from wenet.model.logging_message.message import BaseMessage
from wenet_service_api.common.exception.exceptions import BadRequestException
from wenet_service_api.connector.service_connector import ServiceConnector

logger = logging.getLogger("api.connector.logger_connector")


class LoggerConnector(ServiceConnector):

    @staticmethod
    def build_from_env(extra_headers: Optional[dict] = None) -> LoggerConnector:
        base_url = os.getenv("LOGGER_CONNECTOR_BASE_URL")

        if not base_url:
            raise RuntimeError("ENV: LOGGER_CONNECTOR_BASE_URL is not defined")

        base_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        if extra_headers is not None:
            base_headers.update(extra_headers)

        return LoggerConnector(
            base_url=base_url,
            base_headers=base_headers
        )

    def post_messages(self, messages: List[BaseMessage], headers: Optional[dict] = None) -> List[str]:

        url = f"{self._base_url}/messages"

        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        json_messages = [x.to_repr() for x in messages]

        response = requests.post(url, json=json_messages, headers=headers)

        if response.status_code in [200, 201]:
            return response.json()["traceIds"]
        elif response.status_code == 400:
            raise BadRequestException(response.text)
        else:
            raise Exception(f"Unable to save the log messages server responds [{response.status_code}] [{response.text}]")


class DummyLoggerConnector(LoggerConnector):

    def post_messages(self, messages: List[BaseMessage], headers: Optional[dict] = None) -> List[str]:
        logger.debug("Called logging connector")
        return [
            "1234",
            "5678"
        ]

    @staticmethod
    def build_from_env(extra_headers: Optional[dict] = None) -> LoggerConnector:
        return DummyLoggerConnector("")

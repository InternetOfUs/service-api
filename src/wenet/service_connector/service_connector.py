from __future__ import absolute_import, annotations

from typing import Optional

import abc


class ServiceConnector(abc.ABC):

    def __init__(self, base_url: str, base_headers: Optional[dict] = None):
        self._base_url = base_url
        self._base_headers = base_headers

        if not self._base_headers:
            self._base_headers = {}

    @staticmethod
    def build_from_env() -> ServiceConnector:
        pass

from __future__ import absolute_import, annotations

import logging.config
import os

from wenet_service_api.connector.collector import ServiceConnectorCollector
from wenet_service_api.api.log.logging import get_logging_configuration
from wenet_service_api.api.ws.ws import WsInterface

logging.config.dictConfig(get_logging_configuration("service-api"))

logger = logging.getLogger("api.api.main")


def init_ws() -> WsInterface:

    # Initializations here
    service_connector_collector = ServiceConnectorCollector.build()

    authorized_api_key = os.getenv("APIKEY")
    if authorized_api_key is None:
        raise RuntimeError("Missing environmental variable APIKEY")
    ws_interface = WsInterface(service_connector_collector, authorized_api_key)
    return ws_interface


ws = init_ws()
service_api_app = ws.get_application()

if __name__ == "__main__":
    print(os.getcwd())

    ws.run_server(port=8080)

from __future__ import absolute_import, annotations

import logging.config
import os

from wenet.dao.dao_collector import DaoCollector
from wenet.wenet_service_api.log.logging import get_logging_configuration
from wenet.wenet_service_api.ws.ws import WsInterface

logging.config.dictConfig(get_logging_configuration())

logger = logging.getLogger("wenet.wenet_service_api.main")


def init_ws() -> WsInterface:

    # Initializations here
    dao_collector = DaoCollector.build_from_env()

    authorized_api_key = os.getenv("APIKEY")
    if authorized_api_key is None:
        raise RuntimeError("Missing environmental variable APIKEY")

    ws_interface = WsInterface(dao_collector, authorized_api_key)
    return ws_interface


ws = init_ws()
wenet_service_api = ws.get_application()

if __name__ == "__main__":
    print(os.getcwd())

    ws.run_server(port=8080)

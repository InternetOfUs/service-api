from __future__ import absolute_import, annotations

import logging.config

from wenet.wenet_service_api.log.logging import get_logging_configuration
from wenet.wenet_service_api.ws.ws import WsInterface

logging.config.dictConfig(get_logging_configuration())

logger = logging.getLogger("wenet.wenet_service_api.main")


def init_ws() -> WsInterface:

    # Initializations here

    ws_interface = WsInterface()
    return ws_interface


ws = init_ws()
wenet_service_api = ws.get_application()

if __name__ == "__main__":
    ws.run_server(port=8080)

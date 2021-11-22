from __future__ import absolute_import, annotations

import logging.config
import os
import sentry_sdk

from wenet_service_api.connector.collector import ServiceConnectorCollector
from wenet_service_api.api.log.logging import get_logging_configuration
from wenet_service_api.api.ws.ws import WsInterface
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.flask import FlaskIntegration


logging.config.dictConfig(get_logging_configuration("service-api"))

logger = logging.getLogger("api.api.main")


sentry_logging = LoggingIntegration(
    level=logging.INFO,  # Capture info and above as breadcrumbs
    event_level=logging.ERROR  # Send errors as events
)

sentry_sdk.init(
    integrations=[FlaskIntegration()],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=float(os.getenv("SENTRY_SAMPLE_RATE", "0.1"))
)


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

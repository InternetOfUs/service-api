#!/bin/bash

echo "Verifying env variables presence"
declare -a REQUIRED_ENV_VARS=(
                                  "${PROFILE_MANAGER_CONNECTOR_BASE_URL}"
                                  "${TASK_MANAGER_CONNECTOR_BASE_URL}"
                                  "${HUB_CONNECTOR_BASE_URL}"
                              )

for e in "${REQUIRED_ENV_VARS[@]}"
do
    if [ -z "$e" ]; then
        echo >&2 "Required env variable is missing"
        exit 1
    fi
done

DEFAULT_WORKERS=4
if [ -z "${WORKERS}" ]; then
    WORKERS=$DEFAULT_WORKERS
fi

echo "Running ws"
exec gunicorn -w "${WORKERS}" -b 0.0.0.0:80 "wenet_service_api.api.main:service_api_app"

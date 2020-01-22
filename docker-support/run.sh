#!/bin/bash

echo "Verifying env variables presence"
# TODO enable again when needed
declare -a REQUIRED_ENV_VARS=()
#                                  "${MYSQL_HOST}"
#                                  "${MYSQL_PORT}"
#                                  "${MYSQL_DATABASE}"
#                                  "${MYSQL_USER}"
#                                  "${MYSQL_PASSWORD}"
#                              )

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

echo "Running migrations"
exec gunicorn -w "${WORKERS}" -b 0.0.0.0:80 "wenet.wenet_service_api.main:wenet_service_api"

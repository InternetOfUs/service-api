#!/bin/bash

echo "Verifying env variables presence."
declare -a REQUIRED_ENV_VARS=(
                                "${PLATFORM_BASE_URL}"
                                "${COMP_AUTH_KEY}"
                              )

for e in "${REQUIRED_ENV_VARS[@]}"
do
  if [[ -z "$e" ]]; then
    # TODO should print the missing variable
    echo >&2 "Error: A required env variable is missing."
    exit 1
  fi
done

echo "Running service..."

#
# Important note: env variables should not be passed as arguments to the module!
# This will allow for an easier automatisation of the docker support creation.
#


DEFAULT_WORKERS=4
if [[ -z "${GUNICORN_WORKERS}" ]]; then
    GUNICORN_WORKERS=${DEFAULT_WORKERS}
fi

exec gunicorn -w "${GUNICORN_WORKERS}" -b 0.0.0.0:80 --timeout 60 --graceful-timeout 60 "wenet_service_api.api.main:service_api_app"

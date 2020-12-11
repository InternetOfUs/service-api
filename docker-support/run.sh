#!/bin/bash

echo "Verifying env variables presence."
declare -a REQUIRED_ENV_VARS=(
                                "${PROFILE_MANAGER_CONNECTOR_BASE_URL}"
                                "${TASK_MANAGER_CONNECTOR_BASE_URL}"
                                "${HUB_CONNECTOR_BASE_URL}"
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

exec gunicorn -w "${GUNICORN_WORKERS}" -b 0.0.0.0:80 "wenet_service_api.api.main:service_api_app"

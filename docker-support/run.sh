#!/bin/bash

echo "Verifying env variables presence"
declare -a REQUIRED_ENV_VARS=(
                                  "${DB_CONNECTION_STRING}"
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

echo "Creating manage script for repository"

migrate manage manage.py --repository=migrations --url=$DB_CONNECTION_STRING

echo "Initialize version control of the database"

python manage.py db_version >/dev/null 2>&1
if [ $? != 0 ]; then
  python manage.py version_control
else
  echo " |_ Database already initialized"
fi

echo "Perform migrations"
python manage.py upgrade

echo "Running ws"
exec gunicorn -w "${WORKERS}" -b 0.0.0.0:80 "wenet.wenet_service_api.main:wenet_service_api"

#!/usr/bin/env bash

set -e

python manage.py migrate --noinput
python manage.py test

echo "Starting Gunicorn..."
exec gunicorn mattermost_proxy.wsgi:application -w ${GUNICORN_WORKERS:-12} --bind 0.0.0.0:${SERVER_PORT:-8000}

#!/usr/bin/env bash

python manage.py migrate --noinput
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn ghararpanel.wsgi:application -w ${GUNICORN_WORKERS:-12} --bind 0.0.0.0:${SERVER_PORT:-8000}

#!/bin/sh

set -e

python manage.py collectstatic --noinput

rabbitmq-server &

celery -A doctors_payout worker &

# python manage.py runserver 0.0.0.0:8008

uwsgi --ini /doctors_payout/uwsgi/uwsgi.ini

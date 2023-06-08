#!/bin/sh

set -e

while true; do
  # Check if PostgreSQL server is available
  /py/bin/python /doctors_payout/scripts/check_postgres.py

  if [ $? -eq 0 ]; then
    break  # Break the loop if connection successful
  fi

  sleep 1
done


python manage.py collectstatic --noinput

rabbitmq-server &

celery -A doctors_payout worker &


uwsgi --ini /doctors_payout/uwsgi/uwsgi.ini

# python manage.py runserver 0.0.0.0:8008

#!/bin/sh

set -e


python manage.py collectstatic --noinput

until python -c "import psycopg2; psycopg2.connect('dbname=$POSTGRES_DB user=$POSTGRES_USER host=$POSTGRES_HOST password=$POSTGRES_PASSWORD port=$POSTGRES_PORT')" &>/dev/null; do
    echo "Waiting for PostgreSQL to become available..."
    sleep 1
done

rabbitmq-server &

celery -A doctors_payout worker &


uwsgi --ini /doctors_payout/uwsgi/uwsgi.ini

# python manage.py runserver 0.0.0.0:8008

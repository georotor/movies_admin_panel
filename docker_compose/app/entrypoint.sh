#!/bin/sh

echo -n "Wait DB"
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    echo -n "."
    sleep 0.1
done
echo " started"

python manage.py migrate
python manage.py collectstatic --no-input --clear

exec "$@"

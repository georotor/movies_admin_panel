#!/bin/sh

echo "Wait DB..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 0.1
done
echo "DB started"

python manage.py migrate
python manage.py collectstatic --no-input --clear

exec "$@"
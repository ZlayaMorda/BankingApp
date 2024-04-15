#!/bin/sh
#echo $POSTGRES_DATABASE
#if [ "$POSTGRES_DATABASE" = "postgres" ]
#then
#  echo "Waiting for postgres..."
#
#  while ! [[ $(nc -vz $POSTGRES_HOST $POSTGRES_PORT 2>&1 | grep succeeded) ]]; do
#    echo $(nc -vz $db $POSTGRES_PORT)
#    sleep 0.1
#  done
#
#  echo "PostgreSQL started"
#  python manage.py migrate
#  python manage.py runserver 0.0.0.0:8000
#fi

python manage.py runserver 0.0.0.0:8000
exec "$@"

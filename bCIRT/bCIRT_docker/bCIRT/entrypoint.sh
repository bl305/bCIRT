#!/bin/sh

# if [ "$DATABASE" = "postgres" ]
# then
#     echo "Waiting for postgres..."

#     while ! nc -z $SQL_HOST $SQL_PORT; do
#       sleep 0.1
#     done

#     echo "PostgreSQL started"
# fi

#python3 manage.py flush --no-input
#source /bCIRT/venvs/django_venv/bin/activate
python3 manage.py makemigrations
python3 manage.py migrate
#python3 manage.py syncdb --noinput
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'pass')" | python3 manage.py shell
python3 manage.py initdb -a
python3 manage.py collectstatic --no-input

exec "$@"
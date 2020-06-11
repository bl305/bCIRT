#!/bin/sh
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : bCIRT_docker/entrypoint.sh
# Author            : Balazs Lendvay
# Date created      : 2020.06.08
# Purpose           : entrypoint.sh file for the bCIRT
# Revision History  : v1
# Info              : Ubuntu Bionic 18.04 version for production
# Date        Author      Ref    Description
# 2020.06.08  Lendvay     1      Initial file
# **********************************************************************;

# To create custom database, use this in the database entrypoint
# #!/bin/env bash
# psql -U postgres -c "CREATE USER $DB_USER PASSWORD '$DB_PASS'"
# psql -U postgres -c "CREATE DATABASE $DB_NAME OWNER $DB_USER"


if [ "$bCIRT_DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $bCIRT_SQL_HOST $bCIRT_SQL_PORT; do
      sleep 1
    done

    echo "PostgreSQL started"
fi

/bCIRT/venvs/django_venv/bin/python3 manage.py makemigrations
/bCIRT/venvs/django_venv/bin/python3 manage.py migrate
/bCIRT/venvs/django_venv/bin/python3 manage.py initdb -a

echo yes | python3 manage.py collectstatic --no-input
chown -R www-data:www-data *

echo "HOME: $bCIRT_HOME"
echo "ALLOW: $bCIRT_ALLOWED_HOSTS"
echo "PATH: $bCIRT_PATH"
echo "DB: $bCIRT_DATABASE"
echo "DEBUG: $bCIRT_DEBUG"


exec "$@"

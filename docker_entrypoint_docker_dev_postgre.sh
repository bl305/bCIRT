#!/bin/sh
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : bCIRT_docker/entrypoint.sh
# Author            : Balazs Lendvay
# Date created      : 2020.05.31
# Purpose           : entrypoint.sh file for the bCIRT
# Revision History  : v1
# Info              : Alpine version for development using local sqlite
# Date        Author      Ref    Description
# 2020.05.31  Lendvay     1      Initial file
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

#python3 manage.py flush --no-input
python3 manage.py makemigrations
python3 manage.py migrate
#python3 manage.py syncdb --noinput
#echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'pass')" | python3 manage.py shell
python3 manage.py initdb -a
echo yes | python3 manage.py collectstatic --no-input
echo "HOME: $bCIRT_HOME"
echo "ALLOW: $bCIRT_ALLOWED_HOSTS"
echo "PATH: $bCIRT_PATH"
# echo "SECR: $bCIRT_SECRET_KEY"
# echo "ENC: $bCIRT_ENCRYPTION_KEY_1"
# echo "SALT: $bCIRT_SALT_1"
echo "DB: $bCIRT_DATABASE"
echo "DEBUG: $bCIRT_DEBUG"


exec "$@"

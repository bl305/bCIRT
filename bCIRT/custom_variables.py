# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : bCIRT/custom_variables.py
# Author            : Balazs Lendvay
# Date created      : 2019.07.27
# Purpose           : Custom Settings file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.07.29  Lendvay     1      Initial file
# **********************************************************************;
from os.path import join as path_join
from os import getenv
# from os import environ

# BCIRT_ALLOWED_HOSTS = ['127.0.0.1']
# if getenv("bCIRT_ALLOWED_HOSTS"):
    # BCIRT_ALLOWED_HOSTS = getenv("bCIRT_ALLOWED_HOSTS").split(" ")
BCIRT_ALLOWED_HOSTS = getenv("bCIRT_ALLOWED_HOSTS", '127.0.0.1').split(" ")

# BCIRT_PATH = '/bCIRT/var/www/bCIRT'
# BCIRT_PATH = getenv("bCIRT_PATH", '/bCIRT/var/www/bCIRT')
BCIRT_PATH = getenv("bCIRT_PATH", '/home/bali/PycharmProjects/bCIRT')
# BCIRT_PATH = getenv("bCIRT_PATH", '/bCIRT/var/www/bCIRT')

BCIRT_DEBUG = getenv("bCIRT_DEBUG", False)
# MYMEDIA_ROOT = path_join(BCIRT_PATH, 'media')
BCIRT_MEDIA_ROOT = path_join(BCIRT_PATH, 'media')

# BCIRT_SECRET_KEY = None
BCIRT_SECRET_KEY = getenv("bCIRT_SECRET_KEY", 'moyg9_u$c$gg=0y_ou557!w8kkq7z4ze4_ua*0(l*i(39x*c*p')
# Recommend SecurityNow! grc.com :)
# ENCRYPTION_KEY_1 = "qDqiih0JQgtr6ahdKR0yieQf59MtweBYJ7GbDIA9cWgWBh53cT8j0Zvr1hFsgup"
ENCRYPTION_KEY_1 = getenv("bCIRT_ENCRYPTION_KEY_1", 'qDqiih0JQgtr6ahdKR0yieQf59MtweBYJ7GbDIA9cWgWBh53cT8j0Zvr1hFsgup')
# Should be a 16byte random string in base64 encoded format
# use this site:
# https://nitratine.net/blog/post/encryption-and-decryption-in-python/
# SALT_1 = b'Pr1YFcgFTIQMZERvJf0ySpUEiAniiiRS6NEOkcVbHLQ='
SALT_1 = getenv("bCIRT_ENCRYPTION_KEY_1", b'Pr1YFcgFTIQMZERvJf0ySpUEiAniiiRS6NEOkcVbHLQ=')
# MYDB = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': path_join(BCIRT_PATH, 'db.sqlite3'),
#     }
# }
BCIRT_SQL_DATABASE = None

# if 'BCIRT_SQL_DATABASE' in environ:
if getenv("bCIRT_SQL_DATABASE"):
    # Running the Docker image
    BCIRT_SQL_DATABASE = {
        'default': {
            "ENGINE": getenv("bCIRT_SQL_ENGINE", "django.db.backends.sqlite3"),
            # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
            "NAME": getenv("bCIRT_SQL_DATABASE", path_join(BCIRT_PATH, "db.sqlite3")),
            "USER": getenv("bCIRT_SQL_USER", "user"),
            "PASSWORD": getenv("bCIRT_SQL_PASSWORD", "password"),
            "HOST": getenv("bCIRT_SQL_HOST", "localhost"),
            "PORT": getenv("bCIRT_SQL_PORT", "5432"),
        }
    }
else:
    # Building the Docker image
    BCIRT_SQL_DATABASE = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': path_join(BCIRT_PATH, 'db.sqlite3'),
        }
    }

BASE = 'base.html'
BASE_THEME = 'dark'  # not in use yet
PROJECTNAME = 'bCIRT'
PROJECT_TITLE = 'bCIRT'
TIMEFORMAT = "Y/m/d H:i:s"
LOGLEVEL = 0  # off
# LOGLEVEL = 1 #minimum
# LOGLEVEL = 2 #standard
# LOGLEVEL = 3 #verbose
LOGSEPARATOR = ";"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
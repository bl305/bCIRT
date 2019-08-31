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

MYALLOWED_HOSTS = ['192.168.56.101']

MYPATH = '/home/bali/PycharmProjects/bCIRT'

MYMEDIA_ROOT = path_join(MYPATH, 'media')

# Recommend SecurityNow! grc.com :)
ENCRYPTION_KEY_1 = "qDqiih0JQgtr6ahdKR0yieQf59MtweBYJ7GbDIA9cWgWBh53cT8j0Zvr1hFsgup"
# Should be a 16byte random string in base64 encoded format
# use this site:
# https://nitratine.net/blog/post/encryption-and-decryption-in-python/
SALT_1 = b'Pr1YFcgFTIQMZERvJf0ySpUEiAniiiRS6NEOkcVbHLQ='

MYDB = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': path_join(MYPATH, 'db.sqlite3'),
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

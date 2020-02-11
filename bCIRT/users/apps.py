# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : users/apps.py
# Author            : Balazs Lendvay
# Date created      : 2019.07.27
# Purpose           : Apps file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.07.29  Lendvay     1      Initial file
# **********************************************************************;
from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    # name = 'full.python.path.to.your.app.foo'
    # label = 'my.foo'  # <-- this is the important line - change it to anything other than the default, which is the module name ('foo' in this case)
    # label = 'myusers'

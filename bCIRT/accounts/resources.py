# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : accounts/resources.py
# Author            : Balazs Lendvay
# Date created      : 2019.07.27
# Purpose           : Resources file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.07.29  Lendvay     1      Initial file
# **********************************************************************;
from import_export import resources
from django.contrib.auth.models import User, Group


class UserResource(resources.ModelResource):
    class Meta:
        model = User


class GroupResource(resources.ModelResource):
    class Meta:
        model = Group

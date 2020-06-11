# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : configuration/resources.py
# Author            : Balazs Lendvay
# Date created      : 2019.07.27
# Purpose           : Resources file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.07.29  Lendvay     1      Initial file
# **********************************************************************;
from import_export import resources
from .models import UpdatePackage, ConnectionItem, ConnectionItemField


class UpdatePackageResource(resources.ModelResource):
    class Meta:
        model = UpdatePackage


class ConnectionItemResource(resources.ModelResource):
    class Meta:
        model = ConnectionItem


class ConnectionItemFieldResource(resources.ModelResource):
    class Meta:
        model = ConnectionItemField

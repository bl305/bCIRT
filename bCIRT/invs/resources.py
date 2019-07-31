# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : invs/resources.py
# Author            : Balazs Lendvay
# Date created      : 2019.07.27
# Purpose           : Resources file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.07.29  Lendvay     1      Initial file
# **********************************************************************;
from import_export import resources
from .models import InvAttackvector, \
    InvCategory,\
    InvPriority,\
    InvPhase,\
    InvSeverity,\
    InvStatus,\
    Inv

class InvAttackvectorResource(resources.ModelResource):
    class Meta:
        model = InvAttackvector


class InvCategoryResource(resources.ModelResource):
    class Meta:
        model = InvCategory


class InvPriorityResource(resources.ModelResource):
    class Meta:
        model = InvPriority


class InvPhaseResource(resources.ModelResource):
    class Meta:
        model = InvPhase


class InvSeverityResource(resources.ModelResource):
    class Meta:
        model = InvSeverity


class InvStatusResource(resources.ModelResource):
    class Meta:
        model = InvStatus


class InvResource(resources.ModelResource):
    class Meta:
        model = Inv

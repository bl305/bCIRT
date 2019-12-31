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
from .models import InvAttackVector, \
    InvCategory,\
    InvPriority,\
    InvPhase,\
    InvSeverity,\
    InvStatus,\
    Inv,\
    InvReviewRules,\
    CurrencyType

class InvAttackVectorResource(resources.ModelResource):
    class Meta:
        model = InvAttackVector


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
    # def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        # .sort(parent)
        # print(dataset.sort(2))
        # pass

    class Meta:
        model = Inv

class InvReviewRulesResource(resources.ModelResource):
    class Meta:
        model = InvReviewRules

class CurrencyTypeResource(resources.ModelResource):
    class Meta:
        model = CurrencyType

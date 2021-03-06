# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : invs/admin.py
# Author            : Balazs Lendvay
# Date created      : 2019.07.27
# Purpose           : Admin file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.07.29  Lendvay     1      Initial file
# **********************************************************************;

from django.contrib import admin
# Register your models here.
from . import models
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin


class GroupMemberInline(admin.TabularInline):
    model = models.InvAttackVector
    model = models.InvCategory
    model = models.InvPriority
    model = models.InvPhase
    model = models.InvSeverity
    model = models.InvStatus
    model = models.Inv
    model = models.InvReviewRules
    model = models.CurrencyType
    model = models.InvSeverityCriteria
    model = models.InvSeverityCriteriaCategory
    model = models.InvSeverityContact
    model = models.InvSeverityContactRef

# admin.site.register(models.Inv)
# admin.site.register(models.InvAttackVector)
# admin.site.register(models.InvCategory)
# admin.site.register(models.InvPriority)
# admin.site.register(models.InvPhase)
# admin.site.register(models.InvSeverity)
# admin.site.register(models.InvStatus)


@admin.register(models.CurrencyType)
class CurrencyTypeAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.InvAttackVector)
class InvAttackVectorAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.InvCategory)
class InvCategoryAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.InvPriority)
class InvPriorityAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.InvPhase)
class InvPhaseAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.InvSeverity)
class InvSeverityAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.InvStatus)
class InvStatusAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.Inv)
class InvAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.InvReviewRules)
class InvReviewRulesAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.InvSeverityCriteria)
class InvSeverityCriteriaAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.InvSeverityCriteriaCategory)
class InvSeverityCriteriaCategoryAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.InvSeverityContact)
class InvSeverityContactAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.InvSeverityContactRef)
class InvSeverityContactRefAdmin(ImportExportModelAdmin):
    pass

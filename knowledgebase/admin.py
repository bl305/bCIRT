# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : knowledgebase/admin.py
# Author            : Balazs Lendvay
# Date created      : 2020.03.29
# Purpose           : Admin file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2020.03.29  Lendvay     1      Initial file
# **********************************************************************;

from django.contrib import admin

# Register your models here.
from . import models
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
class GroupMemberInline(admin.TabularInline):
    model = models.KnowledgeBaseFormat
    model = models.KnowledgeBase


@admin.register(models.KnowledgeBaseFormat)
class KnowledgeBaseFormatAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.KnowledgeBase)
class KnowledgeBaseAdmin(ImportExportModelAdmin):
    pass

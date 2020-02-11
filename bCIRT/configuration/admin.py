# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : configuration/admin.py
# Author            : Balazs Lendvay
# Date created      : 2019.07.27
# Purpose           : Admin file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.07.29  Lendvay     1      Initial file
# **********************************************************************;
from django.contrib import admin
from . import models
from import_export.admin import ImportExportModelAdmin
# Register your models here.


class GroupMemberInline(admin.TabularInline):
    model = models.ConnectionItem
    model = models.ConnectionItemField
    model = models.UpdatePackage


@admin.register(models.ConnectionItem)
class ConnectionItemTypeAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.ConnectionItemField)
class ConnectionItemFieldAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.UpdatePackage)
class UpdatePackageAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.SettingsCategory)
class SettingsCategoryAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.SettingsUser)
class SettingsUserAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.SettingsSystem)
class SettingsSystemAdmin(ImportExportModelAdmin):
    pass

# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : accounts/admin.py
# Author            : Balazs Lendvay
# Date created      : 2019.07.27
# Purpose           : Admin file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.07.29  Lendvay     1      Initial file
# **********************************************************************;
from __future__ import unicode_literals
# from django.contrib import admin
from . import models

# Register your models here.
from import_export.admin import ImportExportMixin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from import_export.admin import ImportExportModelAdmin
# from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from django.contrib.auth.models import User, Group
from accounts.resources import UserResource, GroupResource


class GroupMemberInline(admin.TabularInline):
    model = models.UserAudit


class UserAdmin(ImportExportMixin, UserAdmin):
    resource_class = UserResource
    pass


class GroupAdmin(ImportExportMixin, GroupAdmin):
    resource_class = GroupResource
    pass


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)

@admin.register(models.UserAudit)
class UserAuditAdmin(ImportExportModelAdmin):
    pass

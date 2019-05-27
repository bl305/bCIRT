# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# from django.contrib import admin

# Register your models here.
from import_export.admin import ImportExportMixin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
# from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from django.contrib.auth.models import User, Group
from accounts.resources import UserResource, GroupResource


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

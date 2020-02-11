# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : users/admin.py
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

class ProfileInline(admin.TabularInline):
    model = models.Profile


@admin.register(models.Profile)
class ProfileAdmin(ImportExportModelAdmin):
    pass

# from .models import User
# from django.contrib.auth.admin import UserAdmin
# admin.site.register(User, UserAdmin)
from .models import User
from django.contrib.auth.admin import UserAdmin
admin.site.register(User, UserAdmin)



from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
#
# from .forms import CustomUserCreationForm, CustomUserChangeForm
# from .models import CustomUser
#
# class CustomUserAdmin(UserAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = CustomUser
#     list_display = ['email', 'username',]
#
# admin.site.register(CustomUser, CustomUserAdmin)
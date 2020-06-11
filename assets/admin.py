# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : assets/admin.py
# Author            : Balazs Lendvay
# Date created      : 2019.07.27
# Purpose           : Admin file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.07.29  Lendvay     1      Initial file
# **********************************************************************;
# from django.shortcuts import render
from django.contrib import admin
from . import models
from import_export.admin import ImportExportModelAdmin
# Register your models here.


class GroupMemberInline(admin.TabularInline):
    model = models.Profile
    model = models.Host
    model = models.Hostname
    model = models.Ipaddress

# admin.site.register(models.Profile)
# admin.site.register(models.Host)
# admin.site.register(models.Hostname)
# admin.site.register(models.Ipaddress)


@admin.register(models.Profile)
class ProfileAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.Host)
class HostAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.Hostname)
class HostnameAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.Ipaddress)
class IpaddressAdmin(ImportExportModelAdmin):
    pass

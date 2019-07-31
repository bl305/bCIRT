# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : assets/resources.py
# Author            : Balazs Lendvay
# Date created      : 2019.07.27
# Purpose           : Resources file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.07.29  Lendvay     1      Initial file
# **********************************************************************;
# from django.shortcuts import render
from import_export import resources
from .models import Profile, Host, Hostname, Ipaddress


class ProfileResource(resources.ModelResource):
    class Meta:
        model = Profile


class HostResource(resources.ModelResource):
    class Meta:
        model = Host


class HostNameResource(resources.ModelResource):
    class Meta:
        model = Hostname


class IpAddressResource(resources.ModelResource):
    class Meta:
        model = Ipaddress

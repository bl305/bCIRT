# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : reports/urls.py
# Author            : Balazs Lendvay
# Date created      : 2019.07.27
# Purpose           : URL file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.07.29  Lendvay     1      Initial file
# **********************************************************************;
from django.conf.urls import url
from . import views
# from django.contrib.auth import views as auth_views

app_name = 'reports'

urlpatterns = [
    url(r"^$", views.ReportsPage.as_view(), name='rep_base'),

    url(r"dashboard$", views.ReportsDashboardPage.as_view(), name='rep_dashboard'),
    # url(r"monthly$", views.monthly_closed_invs, name='rep_dashboardmonthly'),
    url(r"monthly$", views.ReportsDashboardMonthlyPageMemory.as_view(), name='rep_dashboardmonthly'),
]

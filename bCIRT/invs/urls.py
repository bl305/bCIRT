# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : invs/urls.py
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

app_name = 'invs'

urlpatterns = [

    url(r"^$", views.InvListView.as_view(), name="inv_list"),
    url(r"^new/$", views.InvCreateView.as_view(), name="inv_create"),
    url(r"^detail/(?P<pk>\d+)/$", views.InvDetailView.as_view(), name="inv_detail"),
    url(r'^edit/(?P<pk>\d+)/$', views.InvUpdateView.as_view(), name='inv_edit'),
    url(r'^remove/(?P<pk>\d+)/$', views.InvRemoveView.as_view(), name='inv_remove'),
    url(r'^assign/(?P<pk>\d+)/$', views.InvAssignView.as_view(), name='inv_assign'),

    url(r'^export/pdf/(?P<pk>\d+)', views.MyPDFView.as_view(), name='inv_pdf'),
    url(r"^detailprint/(?P<pk>\d+)/$", views.InvDetailPrintView.as_view(), name="inv_detail_print"),

]

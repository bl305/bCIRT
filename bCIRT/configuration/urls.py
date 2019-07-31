# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : configuration/urls.py
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

app_name = 'configuration'

urlpatterns = [
    url(r"^$", views.ConfigurationPage.as_view(), name='conf_base'),
    url(r"^update/list$", views.UpdatePackageListView.as_view(), name='conf_updatelist'),
    url(r"^update/create$", views.UpdatePackageCreateView.as_view(), name='conf_updatecreate'),
    url(r"^update/detail/(?P<pk>\d+)/$", views.UpdatePackageDetailView.as_view(), name="conf_updatedetail"),
    url(r'^update/edit/(?P<pk>\d+)/$', views.UpdatePackageUpdateView.as_view(), name='conf_updateedit'),
    url(r'^update/remove/(?P<pk>\d+)/$', views.UpdatePackageRemoveView.as_view(), name='conf_updateremove'),
    url(r'^update/install/(?P<pk>\d+)/$',views.InstallPackageRedirectView.as_view(), name="conf_updateinstall"),

    url(r"logging$", views.ConfigurationLoggingPage.as_view(), name='conf_logging'),
]

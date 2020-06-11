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
    url(r"^$", views.ConfigurationPage.as_view(),
        name='conf_base'),
    url(r"^update/list$", views.UpdatePackageListView.as_view(),
        name='conf_updatelist'),
    url(r"^update/create$", views.UpdatePackageCreateView.as_view(),
        name='conf_updatecreate'),
    url(r"^update/detail/(?P<pk>\d+)/$", views.UpdatePackageDetailView.as_view(),
        name="conf_updatedetail"),
    url(r'^update/edit/(?P<pk>\d+)/$', views.UpdatePackageUpdateView.as_view(),
        name='conf_updateedit'),
    url(r'^update/remove/(?P<pk>\d+)/$', views.UpdatePackageRemoveView.as_view(),
        name='conf_updateremove'),
    url(r'^update/install/(?P<pk>\d+)/$', views.InstallPackageRedirectView.as_view(),
        name="conf_updateinstall"),

    url(r"^connectionitem/$", views.ConnectionItemListView.as_view(),
        name="connitem_list"),
    url(r"^connectionitem/new/$", views.ConnectionItemCreateView.as_view(),
        name="connitem_create"),
    url(r"^connectionitem/detail/(?P<pk>\d+)/$", views.ConnectionItemDetailView.as_view(),
        name="connitem_detail"),
    url(r'^connectionitem/edit/(?P<pk>\d+)/$', views.ConnectionItemUpdateView.as_view(),
        name='connitem_edit'),
    url(r'^connectionitem/remove/(?P<pk>\d+)/$', views.ConnectionItemRemoveView.as_view(),
        name='connitem_remove'),

    url(r"^connectionitemfield/$", views.ConnectionItemFieldListView.as_view(),
        name="connitemf_list"),
    url(r"^connectionitemfield/new/$", views.ConnectionItemFieldCreateView.as_view(),
        name="connitemf_create"),
    url(r"^connectionitemfield/detail/(?P<pk>\d+)/$", views.ConnectionItemFieldDetailView.as_view(),
        name="connitemf_detail"),
    url(r'^connectionitemfield/edit/(?P<pk>\d+)/$', views.ConnectionItemFieldUpdateView.as_view(),
        name='connitemf_edit'),
    url(r'^connectionitemfield/remove/(?P<pk>\d+)/$', views.ConnectionItemFieldRemoveView.as_view(),
        name='connitemf_remove'),

    url(r"^settingsuser$", views.SettingsUserListView.as_view(), name='settingsuser_list'),
    url(r'^settingsuser/edit/(?P<pk>\d+)/$', views.SettingsUserUpdateView.as_view(),
        name='settingsuser_edit'),

    url(r"settingssystem$", views.SettingsSystemListView.as_view(), name='settingssystem_list'),
    url(r'^settingssystem/edit/(?P<pk>\d+)/$', views.SettingsSystemUpdateView.as_view(),
        name='settingssystem_edit'),

    url(r"systemupdates$", views.SystemUpdatesPage.as_view(), name='conf_systemupdates'),
    url(r"logging$", views.ConfigurationLoggingPage.as_view(), name='conf_logging'),
    url(r"about$", views.ConfigurationAboutPage.as_view(), name='conf_about'),
]

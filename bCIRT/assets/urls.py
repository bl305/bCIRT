# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : assets/urls.py
# Author            : Balazs Lendvay
# Date created      : 2019.07.27
# Purpose           : URL file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.07.29  Lendvay     1      Initial file
# **********************************************************************;
# from django.shortcuts import render
from django.conf.urls import url
from . import views
# from django.contrib.auth import views as auth_views

app_name = 'assets'

urlpatterns = [
    url(r"^profile$", views.ProfileListView.as_view(), name="prof_list"),
    url(r"^profiles/new/(?P<inv_pk>\d+)/$", views.ProfileCreateView.as_view(), name="prof_create"),
    url(r"^profile/detail/(?P<pk>\d+)/$", views.ProfileDetailView.as_view(), name="prof_detail"),
    url(r'^profile/(?P<pk>\d+)/edit/$', views.ProfileUpdateView.as_view(), name='prof_edit'),
    url(r'^profile/(?P<pk>\d+)/remove/$', views.ProfileRemoveView.as_view(), name='prof_remove'),

    url(r"^profile/autoadd/(?P<inv_pk>\d+)/(?P<evattr_pk>\d+)/(?P<ev_pk>\d+)/$",
        views.ProfileCreateRedirectView.as_view(), name="profile_autoadd"),

    url(r"^host$", views.HostListView.as_view(), name="host_list"),
    url(r"^host/new/$", views.HostCreateView.as_view(), name="host_create"),
    url(r"^host/detail/(?P<pk>\d+)/$", views.HostDetailView.as_view(), name="host_detail"),
    url(r'^host/(?P<pk>\d+)/edit/$', views.HostUpdateView.as_view(), name='host_edit'),
    url(r'^host/(?P<pk>\d+)/remove/$', views.HostRemoveView.as_view(), name='host_remove'),
    #
    # url(r"^hostname$", views.HostnameListView.as_view(), name="hostname_list"),
    # url(r"^hostname/new/$", views.HostnameCreateView.as_view(), name="hostname_create"),
    # url(r"^hostname/detail/(?P<pk>\d+)/$", views.HostnameDetailView.as_view(), name="hostname_detail"),
    # url(r'^hostname/(?P<pk>\d+)/edit/$', views.HostnameUpdateView.as_view(), name='hostname_edit'),
    # url(r'^hostname/(?P<pk>\d+)/remove/$', views.HostnameRemoveView.as_view(), name='hostname_remove'),
    #
    # url(r"^ipaddress$", views.IpaddressListView.as_view(), name="ipaddress_list"),
    # url(r"^ipaddress/new/$", views.IpaddressCreateView.as_view(), name="ipaddress_create"),
    # url(r"^ipaddress/detail/(?P<pk>\d+)/$", views.IpaddressDetailView.as_view(), name="ipaddress_detail"),
    # url(r'^ipaddress/(?P<pk>\d+)/edit/$', views.IpaddressUpdateView.as_view(), name='ipaddress_edit'),
    # url(r'^ipaddress/(?P<pk>\d+)/remove/$', views.IpaddressRemoveView.as_view(), name='ipaddress_remove'),

]

# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : knowledgebase/urls.py
# Author            : Balazs Lendvay
# Date created      : 2020.03.29
# Purpose           : URL file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2020.03.29  Lendvay     1      Initial file
# **********************************************************************;
from django.conf.urls import url
from . import views
# from django.contrib.auth import views as auth_views

app_name = 'knowledgebase'

urlpatterns = [
    url(r"^$", views.KnowledgeBaseListView.as_view(), name="kb_list"),
    url(r"^new/$", views.KnowledgeBaseCreateView.as_view(), name="kb_create"),
    url(r"^detail/(?P<pk>\d+)/$", views.KnowledgeBaseDetailView.as_view(), name="kb_detail"),
    url(r'^edit/(?P<pk>\d+)/$', views.KnowledgeBaseUpdateView.as_view(), name='kb_edit'),
    url(r'^remove/(?P<pk>\d+)/$', views.KnowledgeBaseRemoveView.as_view(), name='kb_remove'),

]

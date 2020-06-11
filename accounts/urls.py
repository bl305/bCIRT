# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : accounts/urls.py
# Author            : Balazs Lendvay
# Date created      : 2019.07.27
# Purpose           : URL file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.07.29  Lendvay     1      Initial file
# **********************************************************************;
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    url(r"^login/$", auth_views.LoginView.as_view(template_name="accounts/account_login.html"), name='login'),
    # url(r"password_reset/$", auth_views.PasswordResetView.as_view(template_name="accounts/account_pw_reset.html"),
    #     name='password_reset'),
    url(r"^logout/$", auth_views.LogoutView.as_view(), name="logout"),
    url(r"^register/$", views.RegisterAccountPage.as_view(), name="register"),
    url(r'^passwordchange/$', views.change_password, name='change_password'),

    url(r"^useraudit/list$", views.UserAuditListView.as_view(),
        name='useraudit_list'),

    #url(r'^passwordchange/$', auth_views.PasswordChangeView.as_view() , name='change_password'),

    # url(r'^passwordchange/done/$', views.PasswordChangeDoneView.as_view(), name='change_password_done'),
]

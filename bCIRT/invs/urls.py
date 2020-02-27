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
# from django.urls import path
urlpatterns = [

    url(r"^$", views.InvListView.as_view(), name="inv_list"),
    url(r"^new/$", views.InvCreateView.as_view(), name="inv_create"),
    url(r"^detail/(?P<pk>\d+)/$", views.InvDetailView.as_view(), name="inv_detail"),
    url(r'^edit/(?P<pk>\d+)/$', views.InvUpdateView.as_view(), name='inv_edit'),
    url(r'^remove/(?P<pk>\d+)/$', views.InvRemoveView.as_view(), name='inv_remove'),
    url(r'^assign/(?P<pk>\d+)/$', views.InvAssignView.as_view(), name='inv_assign'),
    url(r'^review1/(?P<pk>\d+)/$', views.InvReview1UpdateView.as_view(), name='inv_review1'),
    url(r'^review2/(?P<pk>\d+)/$', views.InvReview2UpdateView.as_view(), name='inv_review2'),
    url(r'^review1complete/(?P<pk>\d+)/$', views.InvReview1CompleteView.as_view(), name='inv_review1complete'),
    url(r'^review2complete/(?P<pk>\d+)/$', views.InvReview2CompleteView.as_view(), name='inv_review2complete'),

    url(r'^severities/$', views.InvSeveritiesView.as_view(), name='inv_severities'),

    url(r"^detailtab/(?P<pk>\d+)/$", views.InvTabDetailView.as_view(), name="inv_detailtab"),
    url(r"^profiletab/(?P<pk>\d+)/$", views.InvTabProfileView.as_view(), name="inv_profiletab"),
    url(r"^playbooktab/(?P<pk>\d+)/$", views.InvTabPlaybookView.as_view(), name="inv_playbooktab"),
    url(r"^tasktab/(?P<pk>\d+)/$", views.InvTabTasksView.as_view(), name="inv_tasktab"),
    url(r"^evidencetab/(?P<pk>\d+)/$", views.InvTabEvidencesView.as_view(), name="inv_evidencetab"),

    # url(r'^create/$', views.invaj_create_view, name='invaj_create'),
    url(r'^create/$', views.InvCreateAjaxView.as_view(), name='invaj_create'),
    # url(r'^update/$', views.InvUpdateAjaxView.as_view(), name='invaj_update'),

    # url(r'^export/pdf/(?P<pk>\d+)', views.MyPDFView.as_view(), name='inv_pdf'),
    url(r"^detailprint/(?P<pk>\d+)/$", views.InvDetailPrintView.as_view(), name="inv_detail_print"),
    url(r'^exportinv/(?P<pk>\d+)', views.ExportInvView.as_view(), name='inv_export'),
    url(r'^exportinvfiles/(?P<pk>\d+)', views.ExportInvFilesView.as_view(), name='inv_export_files'),
    # url(r"^detailexport/$", views.exportreviewrules, name="inv_detail_export"),
    # url(r'^simpleupload/$', views.simple_upload, name='simple_upload'),
    url(r'^newsuspiciousemail/$', views.InvSuspiciousEmailCreateView.as_view(), name='inv_suspiciousemail'),

]

# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : bCIRT/views.py
# Author            : Balazs Lendvay
# Date created      : 2019.07.27
# Purpose           : Views file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.07.29  Lendvay     1      Initial file
# 2019.09.06  Lendvay     2      Added session security
# 2019.09.11  Lendvay     3      Fixed recently closed list
# **********************************************************************;
from django.views.generic import TemplateView
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from invs.models import Inv
from tasks.models import Task
# check remaining session time
# from django.contrib.sessions.models import Session
# from datetime import datetime, timezone
# check remaining session time
from django.contrib.auth import get_user_model
User = get_user_model()


# @transaction.atomic
class HomePage(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = "index.html"
    permission_required = ('invs.view_inv', 'tasks.view_task')

    def get_context_data(self, **kwargs):
        kwargs['user'] = self.request.user
        reviewers1 = User.objects.filter(profile__reviewer1=True)
        reviewers1list = set()
        for reviewer1 in reviewers1:
            reviewers1list.add(reviewer1)
        reviewers2 = User.objects.filter(profile__reviewer2=True)
        reviewers2list = set()
        for reviewer2 in reviewers2:
            reviewers2list.add(reviewer2)
        kwargs['reviewers1'] = reviewers1list
        kwargs['reviewers2'] = reviewers2list
        kwargs['invs'] = Inv.objects.filter(user=self.request.user, status=3)[:10]
        kwargs['reviews1'] = Inv.objects.filter(reviewer1=self.request.user, status=5)
        kwargs['reviews2'] = Inv.objects.filter(reviewer2=self.request.user, status=6)
        kwargs['uinvs'] = Inv.objects.exclude(status=3).exclude(status=2)[:10]
        kwargs['oinvs'] = Inv.objects.filter(status=3).exclude(user=self.request.user)[:10]
        kwargs['tasks'] = Task.objects.filter(user=self.request.user)\
            .exclude(status=2)\
            .exclude(type=1)\
            .exclude(status=4)[:10]
        kwargs['utasks'] = Task.objects.filter(status=1)\
            .exclude(type=1)\
            .exclude(status=4)[:10]
        kwargs['otasks'] = Task.objects.exclude(user=self.request.user)\
            .exclude(status=2)\
            .exclude(type=1)\
            .exclude(status=4)[:10]
        kwargs['rtasks'] = Task.objects.filter(user=self.request.user)\
            .exclude(status=1)\
            .exclude(status=3)\
            .exclude(status=5)\
            .order_by('-modified_at')[:10]

        return super(HomePage, self).get_context_data(**kwargs)

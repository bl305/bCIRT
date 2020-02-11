# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : reports/models.py
# Author            : Balazs Lendvay
# Date created      : 2019.07.27
# Purpose           : Models file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.07.29  Lendvay     1      Initial file
# **********************************************************************;
from django.db import models

from django.utils.timezone import timedelta
from invs.models import Inv
from tasks.models import Task
from django.utils.timezone import now as timezone_now
from django.db.models import Count, Avg, Min, Max, Sum  # , F
from tasks.models import EvidenceAttr
from django.db.models import Q


def durationprint(timevalue=None):
    # retval = "-"
    if timevalue is not None:
        tduration = timevalue
        day = int(tduration // (24 * 3600))
        tduration = tduration % (24 * 3600)
        hour = int(tduration // 3600)
        tduration %= 3600
        minutes = int(tduration // 60)
        tduration %= 60
        seconds = int(tduration)
        retval = str(day)+"d"+str(hour)+"h"+str(minutes)+"m"+str(seconds)+"s"
    elif timevalue == 0:
        retval = 0
    else:
        retval = "-"
    return retval


class Get_Report():
    def __init__(self, astart=None, aend=None):
        self.astart = astart
        if astart is None:
            self.astart = timezone_now() - timedelta(days=30)
            # self.astart = datetime.now() - timedelta(days=30)
        self.aend = aend
        if aend is None:
            self.aend = timezone_now()
            # self.aend = datetime.now()

    def invs_all(self):
        retval = Inv.objects.filter(created_at__gte=self.astart)\
            .filter(created_at__lte=self.aend) \
            .values('status__name')\
            .annotate(Count('status'))\
            .order_by('status__name')
        return retval

    def invs_closed_by_user_all(self):
        retval = Inv.objects.filter(created_at__gte=self.astart)\
            .filter(created_at__lte=self.aend) \
            .filter(status=2) \
            .values('user__username')\
            .annotate(Count('user'))\
            .order_by('user__username')
        return retval


    def invs_closed(self):
        retval = Inv.objects.filter(created_at__gte=self.astart)\
            .filter(created_at__lte=self.aend) \
            .filter(status=2) \
            .values('status__name')\
            .annotate(Count('status'))\
            .order_by('status__name')
        return retval

    def phishing_malicious_attachments(self):
        retval = EvidenceAttr.objects \
            .filter(attr_reputation__name='Malicious') \
            .filter(Q(evattrformat__name__startswith='Hash_') | Q(evattrformat__name='FileName')) \
            .filter(ev__inv__attackvector__name='Phishing') \
            .filter(ev__inv__status=2) \
            .values_list('ev__inv__created_at', 'ev__inv') \
            .distinct() \
            .order_by('ev__inv')

        return retval

    def invs_all_summary(self):
        retval = Inv.objects.filter(created_at__gte=self.astart)\
            .filter(created_at__lte=self.aend) \
            .exclude(summary="Suspicious email")\
            .exclude(summary=None)\
            .values('summary', 'id', 'created_at')\
            .annotate(total=Count('id'))\
            .order_by('summary')

        return retval

    def invduration(self):
        invduration_values = Inv.objects.filter(created_at__gte=self.astart)\
            .filter(created_at__lte=self.aend)\
            .filter(status=2) \
            .aggregate(Min('invduration'), Max('invduration'), Avg('invduration'))
        invs_closed_stats_min = durationprint(invduration_values['invduration__min'])
        invs_closed_stats_avg = durationprint(invduration_values['invduration__avg'])
        invs_closed_stats_max = durationprint(invduration_values['invduration__max'])
        retval = {'min': invs_closed_stats_min,
                  'max': invs_closed_stats_max,
                  'avg': invs_closed_stats_avg}
        return retval

    def invs_closed_tasks(self, atype=None):
        if atype == "Manual":
            inv_closed_tasks = Inv.objects.filter(created_at__gte=self.astart) \
                .filter(created_at__lte=self.aend) \
                .filter(status=2) \
                .filter(task_inv__type=2) \
                .values('pk') \
                .annotate(Count('task_inv')) \
                .order_by('pk') \
                .aggregate(Min('task_inv__count'), Avg('task_inv__count'), Max('task_inv__count'))
        elif atype == "Auto":
            inv_closed_tasks = Inv.objects.filter(created_at__gte=self.astart) \
                .filter(created_at__lte=self.aend) \
                .filter(status=2) \
                .filter(task_inv__type=1) \
                .values('pk') \
                .annotate(Count('task_inv')) \
                .order_by('pk') \
                .aggregate(Min('task_inv__count'), Avg('task_inv__count'), Max('task_inv__count'))
        else:
            inv_closed_tasks = Inv.objects.filter(created_at__gte=self.astart)\
                .filter(created_at__lte=self.aend) \
                .filter(status=2) \
                .values('pk') \
                .annotate(Count('task_inv')) \
                .order_by('pk') \
                .aggregate(Min('task_inv__count'), Avg('task_inv__count'), Max('task_inv__count'))

        if inv_closed_tasks['task_inv__count__min']:
            amin = int(inv_closed_tasks['task_inv__count__min'])
        else:
            amin = 0
        if inv_closed_tasks['task_inv__count__avg']:
            aavg = round(inv_closed_tasks['task_inv__count__avg'])
        else:
            aavg = 0
        if inv_closed_tasks['task_inv__count__max']:
            amax = int(inv_closed_tasks['task_inv__count__max'])
        else:
            amax = 0
        retval = {'min': amin,
                  'max': amax,
                  'avg': aavg}
        return retval

    def tasks_all(self):
        retval = Task.objects.filter(created_at__gte=self.astart)\
            .filter(created_at__lte=self.aend) \
            .values('status__name')\
            .annotate(Count('status'))\
            .order_by('status__name')
        return retval

    def tasks_closed(self):
        retval = Task.objects.filter(created_at__gte=self.astart)\
            .filter(created_at__lte=self.aend) \
            .filter(status=2) \
            .values('status__name')\
            .annotate(Count('status'))\
            .order_by('status__name')
        return retval

    def taskduration(self, atype=None):
        if atype == "Manual":
            taskduration_values = Task.objects.filter(created_at__gte=self.astart)\
                .filter(created_at__lte=self.aend)\
                .filter(type__name='Manual') \
                .filter(status=2) \
                .aggregate(Min('taskduration'), Max('taskduration'), Avg('taskduration'))
        elif atype == "Auto":
            taskduration_values = Task.objects.filter(created_at__gte=self.astart)\
                .filter(created_at__lte=self.aend)\
                .filter(type__name='Auto') \
                .filter(status=2) \
                .aggregate(Min('taskduration'), Max('taskduration'), Avg('taskduration'))
        else:
            taskduration_values = Task.objects.filter(created_at__gte=self.astart)\
                .filter(created_at__lte=self.aend)\
                .filter(status=2) \
                .aggregate(Min('taskduration'), Max('taskduration'), Avg('taskduration'))

        tasks_closed_stats_min = durationprint(taskduration_values['taskduration__min'])
        tasks_closed_stats_avg = durationprint(taskduration_values['taskduration__avg'])
        tasks_closed_stats_max = durationprint(taskduration_values['taskduration__max'])
        retval = {'min': tasks_closed_stats_min,
                  'max': tasks_closed_stats_max,
                  'avg': tasks_closed_stats_avg}
        return retval

    def attackvector(self):
        retval = Inv.objects.filter(created_at__gte=self.astart)\
            .filter(created_at__lte=self.aend)\
            .filter(status=2)\
            .values('attackvector__name')\
            .annotate(Count('attackvector'))\
            .order_by('attackvector__name')
        return retval

    def attackvector_victims(self):
        retval = Inv.objects.filter(created_at__gte=self.astart)\
            .filter(created_at__lte=self.aend)\
            .filter(status=2)\
            .values('attackvector__name')\
            .annotate(Sum('numofvictims'))\
            .order_by('attackvector__name')
        return retval

    def attackvector_stats(self):
        retval = Inv.objects.filter(created_at__gte=self.astart)\
            .filter(created_at__lte=self.aend)\
            .filter(status=2) \
            .values('attackvector__name', 'losscurrency__currencyshortname')\
            .annotate(potential=Sum('potentialloss'), monetary=Sum('monetaryloss'))\
            .order_by('attackvector__name') \
            .filter(Q(potential__gt=0) | Q(monetary__gt=0))
        return retval

    def phishing_stats(self):
        retval = Inv.objects.filter(created_at__gte=self.astart)\
            .filter(created_at__lte=self.aend)\
            .filter(status=2) \
            .filter(attackvector__name='Phishing') \
            .values('pk', 'losscurrency__currencyshortname')\
            .annotate(potential=Sum('potentialloss'), monetary=Sum('monetaryloss'))\
            .filter(Q(potential__gt=0) | Q(monetary__gt=0))
        return retval

    def tasks_closed_title(self):
        retval = Task.objects.filter(created_at__gte=self.astart)\
            .filter(created_at__lte=self.aend) \
            .filter(status=2) \
            .values('title')\
            .annotate(Count('title'))\
            .order_by('-title__count')
        return retval

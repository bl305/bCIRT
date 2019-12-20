# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : reports/view.py
# Author            : Balazs Lendvay
# Date created      : 2019.07.27
# Purpose           : View file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.07.29  Lendvay     1      Initial file
# 2019.09.06  Lendvay     2      Added session security
# **********************************************************************;
from django.views.generic import TemplateView  # , View
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)

from django.utils.timezone import timedelta
from invs.models import Inv
from tasks.models import Task
from reports.forms import CustomReportForm
from bCIRT.settings import ALLOWED_HOSTS
# from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from pytz import timezone
from datetime import datetime

from django.shortcuts import redirect, reverse  # ,render, get_object_or_404
from django.contrib import messages
from django.utils.http import is_safe_url
# from django.contrib.sessions.models import Session
# from datetime import datetime, timezone
from django.db.models.functions import Concat
from django.db.models import CharField  # , Value as V
from django.db.models.functions.datetime import ExtractMonth, ExtractYear

from django.utils.timezone import now as timezone_now
from django.db.models import Count, Avg, Min, Max, Sum  # , F
from bCIRT.custom_variables import LOGSEPARATOR, LOGLEVEL
from django.shortcuts import render
import pygal
from tasks.models import EvidenceAttr
from django.db.models import Q

import logging
logger = logging.getLogger('log_file_verbose')


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


class ReportsPage(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'reports/reports_base.html'
    permission_required = ('invs.view_inv',)

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(ReportsPage, self).__init__(*args, **kwargs)


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
            .values('summary', 'id')\
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


class ReportsDashboardPage(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'reports/reports_dashboard.html'
    permission_required = ('invs.view_inv', 'tasks.view_task')
    utc = timezone("UTC")
    nowtime = datetime.now()
    # dataendtime = datetime.strftime(rawendtime,newformat)
    endtime = utc.localize(nowtime)
    searchendtime = endtime
    # alltime = datetime.now()-timedelta(days=25000)
    # last30days = datetime.now()-timedelta(days=30)
    # last90days = datetime.now()-timedelta(days=90)

    alltime = endtime-timedelta(days=25000)
    last30days = endtime-timedelta(days=30)
    last90days = endtime-timedelta(days=90)
    # starttime30 = utc.localize(last30days)
    # starttime90 = utc.localize(last90days)
    starttime30 = last30days
    starttime90 = last90days

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(ReportsDashboardPage, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['user'] = self.request.user
        # Closed investigations
        kwargs['invs_closed'] = Get_Report(self.alltime, self.searchendtime).invs_all()
        kwargs['invs_closed_30'] = Get_Report(self.starttime30, self.searchendtime).invs_all()
        kwargs['invs_closed_90'] = Get_Report(self.starttime90, self.searchendtime).invs_all()

        invs_closed_stats = Get_Report(self.alltime, self.searchendtime).invduration()
        kwargs['invs_closed_stats_min'] = invs_closed_stats['min']
        kwargs['invs_closed_stats_max'] = invs_closed_stats['max']
        kwargs['invs_closed_stats_avg'] = invs_closed_stats['avg']

        invs_closed_stats30 = Get_Report(self.starttime30, self.searchendtime).invduration()
        kwargs['invs_closed_stats30_min'] = invs_closed_stats30['min']
        kwargs['invs_closed_stats30_max'] = invs_closed_stats30['max']
        kwargs['invs_closed_stats30_avg'] = invs_closed_stats30['avg']

        invs_closed_stats90 = Get_Report(self.starttime90, self.searchendtime).invduration()
        kwargs['invs_closed_stats90_min'] = invs_closed_stats90['min']
        kwargs['invs_closed_stats90_max'] = invs_closed_stats90['max']
        kwargs['invs_closed_stats90_avg'] = invs_closed_stats90['avg']

        invs_closed_tasks = Get_Report(self.alltime, self.searchendtime).invs_closed_tasks()
        kwargs['invs_closed_tasks_min'] = invs_closed_tasks['min']
        kwargs['invs_closed_tasks_max'] = invs_closed_tasks['max']
        kwargs['invs_closed_tasks_avg'] = invs_closed_tasks['avg']
        invs_closed_tasks_manual = Get_Report(self.starttime30, self.searchendtime).invs_closed_tasks(atype="Manual")
        kwargs['invs_closed_tasks_manual_min'] = invs_closed_tasks_manual['min']
        kwargs['invs_closed_tasks_manual_max'] = invs_closed_tasks_manual['max']
        kwargs['invs_closed_tasks_manual_avg'] = invs_closed_tasks_manual['avg']
        invs_closed_tasks_auto = Get_Report(self.starttime90, self.searchendtime).invs_closed_tasks(atype="Auto")
        kwargs['invs_closed_tasks_auto_min'] = invs_closed_tasks_auto['min']
        kwargs['invs_closed_tasks_auto_max'] = invs_closed_tasks_auto['max']
        kwargs['invs_closed_tasks_auto_avg'] = invs_closed_tasks_auto['avg']

        kwargs['tasks_closed'] = Get_Report(self.alltime, self.searchendtime).tasks_all()
        kwargs['tasks_closed_30'] = Get_Report(self.starttime30, self.searchendtime).tasks_all()
        kwargs['tasks_closed_90'] = Get_Report(self.starttime90, self.searchendtime).tasks_all()

        task_duration = Get_Report(self.alltime, self.searchendtime).taskduration()
        kwargs['tasks_closed_stats_min'] = task_duration['min']
        kwargs['tasks_closed_stats_max'] = task_duration['max']
        kwargs['tasks_closed_stats_avg'] = task_duration['avg']

        task_duration30 = Get_Report(self.starttime30, self.searchendtime).taskduration()
        kwargs['tasks_closed_stats30_min'] = task_duration30['min']
        kwargs['tasks_closed_stats30_max'] = task_duration30['max']
        kwargs['tasks_closed_stats30_avg'] = task_duration30['avg']

        task_duration90 = Get_Report(self.starttime90, self.searchendtime).taskduration()
        kwargs['tasks_closed_stats90_min'] = task_duration90['min']
        kwargs['tasks_closed_stats90_max'] = task_duration90['max']
        kwargs['tasks_closed_stats90_avg'] = task_duration90['avg']

        kwargs['tasks_manual_closed'] = Get_Report(self.alltime, self.searchendtime).taskduration()
        kwargs['tasks_manual_closed_30'] = Get_Report(self.starttime30, self.searchendtime).taskduration()
        kwargs['tasks_manual_closed_90'] = Get_Report(self.starttime90, self.searchendtime).taskduration()

        taskduration_manual = Get_Report(self.alltime, self.searchendtime).taskduration(atype="Manual")
        kwargs['tasks_manual_closed_stats_min'] = taskduration_manual['min']
        kwargs['tasks_manual_closed_stats_max'] = taskduration_manual['max']
        kwargs['tasks_manual_closed_stats_avg'] = taskduration_manual['avg']

        taskduration_manual_30 = Get_Report(self.starttime30, self.searchendtime).taskduration(atype="Manual")
        kwargs['tasks_manual_closed_stats30_min'] = taskduration_manual_30['min']
        kwargs['tasks_manual_closed_stats30_max'] = taskduration_manual_30['max']
        kwargs['tasks_manual_closed_stats30_avg'] = taskduration_manual_30['avg']

        taskduration_manual_90 = Get_Report(self.starttime90, self.searchendtime).taskduration(atype="Manual")
        kwargs['tasks_manual_closed_stats90_min'] = taskduration_manual_90['min']
        kwargs['tasks_manual_closed_stats90_max'] = taskduration_manual_90['max']
        kwargs['tasks_manual_closed_stats90_avg'] = taskduration_manual_90['avg']

        kwargs['invs_closed_attackvector'] = Get_Report(self.alltime, self.searchendtime).attackvector()
        kwargs['invs_closed_attackvector_30'] = Get_Report(self.starttime30, self.searchendtime).attackvector()
        kwargs['invs_closed_attackvector_90'] = Get_Report(self.starttime90, self.searchendtime).attackvector()

        kwargs['phish_closed_stats'] = Get_Report(self.alltime, self.searchendtime).phishing_stats()
        kwargs['phish_closed_stats_30'] = Get_Report(self.starttime30, self.searchendtime).phishing_stats()
        kwargs['phish_closed_stats_90'] = Get_Report(self.starttime90, self.searchendtime).phishing_stats()

        return super(ReportsDashboardPage, self).get_context_data(**kwargs)


class ReportsDashboardMonthlyPageMemory(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'reports/reports_monthly.html'
    permission_required = ('invs.view_inv', 'tasks.view_task')

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(ReportsDashboardMonthlyPageMemory, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ReportsDashboardMonthlyPageMemory, self).get_context_data(**kwargs)
        kwargs['user'] = self.request.user
        retval = dict()
        data_invsclosed = reports_dashboard_monthly_invsclosed()
        data_invsclosed_by_attackvector = reports_dashboard_monthly_invsattackvector()
        data_invsclosed_by_attackvector_phishingmalware = reports_dashboard_monthly_invsattackvector_phishingmalware()
        retval.update(data_invsclosed)
        retval.update(data_invsclosed_by_attackvector)
        retval.update(data_invsclosed_by_attackvector_phishingmalware)
        # context['graph_data_invclosed'] = displaydata['graph_data_invclosed']
        # context['graph_table_invclosed'] = displaydata['graph_table_invclosed']
        # context['graph_data_attackvectorclosed'] = displaydata['graph_data_attackvectorclosed']
        # context['graph_table_attackvectorclosed'] = displaydata['graph_table_attackvectorclosed']
        return retval


def reports_dashboard_monthly_invsclosed():
    invsource = Inv.objects.filter(status__name='Closed'). \
        annotate(
        mydate=Concat(ExtractYear('created_at'), ExtractMonth('created_at'), output_field=CharField())). \
        values_list('mydate'). \
        values('mydate'). \
        annotate(count=Count('mydate')). \
        order_by('mydate', 'count')

    invstattable = list()
    for invitems in invsource:
        newitem = "%s%s" % (invitems['mydate'][0:4], '{:02d}'.format(int(invitems['mydate'][4:])))
        # invstattable.append((invitems['mydate'], invitems['count']))
        invstattable.append((newitem, invitems['count']))
    b_chart = pygal.Bar()
    b_chart.title = "Closed Investigations by Month"
    # b_chart.x_labels = map(str, range(201908, 201910))

    for onebar in invstattable:
        b_chart.add(onebar[0], [onebar[1]])
    invstat_data = b_chart.render_data_uri()

    return {'graph_data_invclosed': invstat_data, 'graph_table_invclosed': invstattable}


def reports_dashboard_monthly_invsattackvector():
    # ## testing
    # .filter(created_at__gt=timezone_now() - timedelta(days=30)) \
    attackvectorsource = Inv.objects\
        .filter(status=2) \
        .annotate(
            mydate=Concat(ExtractYear('created_at'), ExtractMonth('created_at'), output_field=CharField())) \
        .values_list('mydate') \
        .values('mydate', 'attackvector__name') \
        .annotate(count=Count('mydate')) \
        .order_by('mydate', 'count')

    attackvectorstattable = list()
    attackvectornames = set()
    attackvectordates = set()
    for attackvectoritems in attackvectorsource:
        newitem = "%s%s" % (attackvectoritems['mydate'][0:4], '{:02d}'.format(int(attackvectoritems['mydate'][4:])))
        # attackvectorstattable.append(
        #     (attackvectoritems['mydate'], attackvectoritems['attackvector__name'], attackvectoritems['count']))
        # attackvectornames.add(attackvectoritems['attackvector__name'])
        # attackvectordates.add(attackvectoritems['mydate'])
        attackvectorstattable.append(
            (newitem, attackvectoritems['attackvector__name'], attackvectoritems['count']))
        attackvectornames.add(attackvectoritems['attackvector__name'])
        attackvectordates.add(newitem)

    c_chart = pygal.StackedBar()
    c_chart.title = "Closed Investigations by AttackVector by Month"

    attackvectordateslist = list(attackvectordates)
    attackvectordateslist.sort()
    c_chart.x_labels = map(str, attackvectordateslist)
    attackvectorline = dict()
    mychartline = dict()
    attackvectordatelength = len(attackvectordateslist)
    if attackvectordatelength:

        # different grouping
        for attackvectorname in attackvectornames:
            attackvectorline[attackvectorname] = []
            mychartline[attackvectorname] = []
            for attackvectordate in attackvectordateslist:
                # print("NAME:%s Date:%s"%(attackvectorname, attackvectordate))
                for i in attackvectorstattable:
                    if i[0] == attackvectordate and i[1] == attackvectorname:
                        attackvectorline[attackvectorname] += [i[0], i[2]],
    # generate an empty dictionary
    for attackvectorname in attackvectornames:
        for attackvectordate in attackvectordateslist:
            mychartline[attackvectorname] += {attackvectordate: None},
    # check if there is data available for each dictionary item
    for akey, avalue in attackvectorline.items():
        if avalue:
            for avalueitem in avalue:
                for recnum in range(len(mychartline[akey])):
                    if mychartline[akey][recnum]:
                        for mkey, mval in mychartline[akey][recnum].items():
                            if avalueitem[0] == mkey:
                                mychartline[akey][recnum][avalueitem[0]] = avalueitem[1]

    for akey, avalue in mychartline.items():
        finlist = list()
        for avalueitem in avalue:
            for ikey, ivalue in avalueitem.items():
                finlist.append(ivalue)
        c_chart.add(akey, finlist)

    attackvectorstat_data = c_chart.render_data_uri()
    return {'graph_data_attackvectorclosed': attackvectorstat_data,
            'graph_table_attackvectorclosed': attackvectorstattable}


def reports_dashboard_monthly_invsattackvector_phishingmalware():
    '''
    This function checks if a phishing incident contains any malicious hashes or filenames
    :return:
    '''
    countofmalicious = EvidenceAttr.objects\
        .filter(attr_reputation__name='Malicious')\
        .filter(Q(evattrformat__name__startswith='Hash_') | Q(evattrformat__name='FileName'))\
        .filter(ev__inv__attackvector__name='Phishing')\
        .filter(ev__inv__status=2)\
        .annotate(
            mydate=Concat(ExtractYear('ev__inv__created_at'), ExtractMonth('ev__inv__created_at'), output_field=CharField())) \
        .values_list('mydate', 'ev__inv')\
        .distinct()\
        .order_by('mydate')
    countofmalicioustable = list()
    tmplist = list()
    tmpnames = set()
    for items in countofmalicious:
        newitem = "%s%s" % (items[0][0:4], '{:02d}'.format(int(items[0][4:])))
        # tmplist.append(items[0])
        # tmpnames.add(items[0])
        tmplist.append(newitem)
        tmpnames.add(newitem)
    b_chart = pygal.Bar()
    b_chart.title = "Phishing emails malware attachment by Month"
    for tmpname in tmpnames:
        b_chart.add(tmpname, tmplist.count(tmpname))
        countofmalicioustable.append((tmpname, tmplist.count(tmpname)))
    countofmalicioustable.sort()
    countofmalicious_data = b_chart.render_data_uri()

    return {'graph_data_attackvectorphishingmalware': countofmalicious_data,
            'graph_table_attackvectorphishingmalware': countofmalicioustable}


class ReportsDashboardCustom(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'reports/reports_custom.html'
    permission_required = ('invs.view_inv', 'tasks.view_task')
    form_class = CustomReportForm
    initial = {'key': 'value'}
    success_url = reverse_lazy('reports:rep_dashboardcustom')

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(ReportsDashboardCustom, self).__init__(*args, **kwargs)

    def get_initial(self):
        initial = super(ReportsDashboardCustom, self).get_initial()
        if self.request.user.is_authenticated:
            initial.update({'name': self.request.user.get_full_name()})
        return initial

    def get(self, request, *args, **kwargs):
        form = CustomReportForm()
        context = {'form': form}
        return render(request, 'reports/reports_custom.html', context)

    def post(self, request, *args, **kwargs):
        form = CustomReportForm(data=request.POST)
        pickerformat = "%Y-%m-%d %H:%M:%S"
        # dateformat = "%Y-%m-%d %H:%M"
        # datetimenowformat = "%m/%d/%Y %H:%M"
        # newformat = "%Y-%m-%d %H:%M%z"
        if form.is_valid():
            # self.send_mail(form.cleaned_data)
            utc = timezone("UTC")
            # searchstarttime = None
            # searchendtime = None
            if form.data:
                datatmp = form.data
                if datatmp['starttime'] == '':
                    rawstarttime = datetime.now()-timedelta(days=25000)
                    # datastarttime = datetime.strftime(rawstarttime,newformat)
                    starttime = utc.localize(rawstarttime)
                    searchstarttime = starttime
                else:
                    datastarttime = datatmp['starttime']
                    starttime = datetime.strptime((datastarttime), pickerformat)
                    starttime = utc.localize(starttime)
                    searchstarttime = starttime
                if datatmp['endtime'] == '':
                    rawendtime = datetime.now()
                    # dataendtime = datetime.strftime(rawendtime,newformat)
                    endtime = utc.localize(rawendtime)
                    searchendtime = endtime
                else:
                    dataendtime = datatmp['endtime']
                    endtime = datetime.strptime((dataendtime), pickerformat)
                    endtime = utc.localize(endtime)
                    searchendtime = endtime

                form = CustomReportForm()
                # last0days = datetime.now()
                # last30days = datetime.now()-timedelta(days=30)
                # last90days = datetime.now()-timedelta(days=90)
                invs_closed = Get_Report(searchstarttime, searchendtime).invs_closed()
                invs_all_summary = Get_Report(searchstarttime, searchendtime).invs_all_summary()
                invs_closed_stats = Get_Report(searchstarttime, searchendtime).invduration()
                invs_closed_stats_min = invs_closed_stats['min']
                invs_closed_stats_max = invs_closed_stats['max']
                invs_closed_stats_avg = invs_closed_stats['avg']
                invs_closed_tasks = Get_Report(searchstarttime, searchendtime).invs_closed_tasks()
                invs_closed_tasks_min = invs_closed_tasks['min']
                invs_closed_tasks_max = invs_closed_tasks['max']
                invs_closed_tasks_avg = invs_closed_tasks['avg']
                invs_closed_tasks_manual = Get_Report(searchstarttime, searchendtime).invs_closed_tasks(atype="Manual")
                invs_closed_tasks_manual_min = invs_closed_tasks_manual['min']
                invs_closed_tasks_manual_max = invs_closed_tasks_manual['max']
                invs_closed_tasks_manual_avg = invs_closed_tasks_manual['avg']
                invs_closed_tasks_auto = Get_Report(searchstarttime, searchendtime).invs_closed_tasks(atype="Auto")
                invs_closed_tasks_auto_min = invs_closed_tasks_auto['min']
                invs_closed_tasks_auto_max = invs_closed_tasks_auto['max']
                invs_closed_tasks_auto_avg = invs_closed_tasks_auto['avg']
                tasks_closed = Get_Report(searchstarttime, searchendtime).tasks_closed()
                tasks_closed_stats = Get_Report(searchstarttime, searchendtime).taskduration()
                tasks_closed_stats_min = tasks_closed_stats['min']
                tasks_closed_stats_max = tasks_closed_stats['max']
                tasks_closed_stats_avg = tasks_closed_stats['avg']
                tasks_manual_closed_stats = Get_Report(searchstarttime, searchendtime).taskduration(atype="Manual")
                tasks_manual_closed_stats_min = tasks_manual_closed_stats['min']
                tasks_manual_closed_stats_max = tasks_manual_closed_stats['max']
                tasks_manual_closed_stats_avg = tasks_manual_closed_stats['avg']
                invs_closed_attackvector = Get_Report(searchstarttime, searchendtime).attackvector()
                invs_closed_attackvector_victims = Get_Report(searchstarttime, searchendtime).attackvector_victims()
                phish_closed_stats = Get_Report(searchstarttime, searchendtime).phishing_stats()
                attackvector_stats = Get_Report(searchstarttime, searchendtime).attackvector_stats()
                tasks_closed_title = Get_Report(searchstarttime, searchendtime).tasks_closed_title()
                phishing_malicious_attachments = Get_Report(searchstarttime, searchendtime).\
                    phishing_malicious_attachments()

                context = {'form': form,
                           'starttime': starttime,
                           'endtime': endtime,
                           'searchstarttime': searchstarttime,
                           'searchendtime': searchendtime,
                           'invs_closed': invs_closed,
                           'invs_all_summary': invs_all_summary,
                           'invs_closed_stats_min': invs_closed_stats_min,
                           'invs_closed_stats_max': invs_closed_stats_max,
                           'invs_closed_stats_avg': invs_closed_stats_avg,
                           'invs_closed_tasks_min': invs_closed_tasks_min,
                           'invs_closed_tasks_max': invs_closed_tasks_max,
                           'invs_closed_tasks_avg': invs_closed_tasks_avg,
                           'invs_closed_tasks_manual_min': invs_closed_tasks_manual_min,
                           'invs_closed_tasks_manual_max': invs_closed_tasks_manual_max,
                           'invs_closed_tasks_manual_avg': invs_closed_tasks_manual_avg,
                           'invs_closed_tasks_auto_min': invs_closed_tasks_auto_min,
                           'invs_closed_tasks_auto_max': invs_closed_tasks_auto_max,
                           'invs_closed_tasks_auto_avg': invs_closed_tasks_auto_avg,
                           'tasks_closed': tasks_closed,
                           'tasks_closed_stats_min': tasks_closed_stats_min,
                           'tasks_closed_stats_max': tasks_closed_stats_max,
                           'tasks_closed_stats_avg': tasks_closed_stats_avg,
                           'tasks_manual_closed_stats_min': tasks_manual_closed_stats_min,
                           'tasks_manual_closed_stats_max': tasks_manual_closed_stats_max,
                           'tasks_manual_closed_stats_avg': tasks_manual_closed_stats_avg,
                           'invs_closed_attackvector': invs_closed_attackvector,
                           'invs_closed_attackvector_victims': invs_closed_attackvector_victims,
                           'phish_closed_stats': phish_closed_stats,
                           'attackvector_stats': attackvector_stats,
                           'tasks_closed_title': tasks_closed_title,
                           'phishing_malicious_attachments': phishing_malicious_attachments,
                           }
            else:
                context = {'': ''}
            return render(request, 'reports/reports_custom.html', context)
        return render(request, 'reports/reports_custom.html', {'form': form})

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        # context = super(ReportsDashboardCustom, self).get_context_data(**kwargs)
        kwargs['user'] = self.request.user

        return super(ReportsDashboardCustom, self).get_context_data(**kwargs)

    def form_valid(self, form):
        cleandata = form.cleaned_data
        return super(ReportsDashboardCustom, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('invs.add_inv'):
            messages.error(self.request, "No permission to add a record !!!")
            return redirect('invs:inv_list')
        else:
            pass
        # Checks pass, let http method handlers process the request
        return super(ReportsDashboardCustom, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(ReportsDashboardCustom, self).get_form_kwargs()
        # Update the kwargs with the user_id
        # kwargs['inv_pk'] = self.kwargs.get('inv_pk')
        kwargs['user'] = self.request.user
        return kwargs

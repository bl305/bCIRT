from django.views.generic import TemplateView
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)

from django.utils.timezone import timedelta
from invs.models import Inv
from tasks.models import Task
from django.contrib.sessions.models import Session
from datetime import datetime, timezone
from django.utils.timezone import now as timezone_now
from django.db.models import Count, Avg, Min, Max
import logging
logger = logging.getLogger('log_file_verbose')


def durationprint(timevalue=None):
    if timevalue:
        tduration = timevalue
        day = int(tduration // (24 * 3600))
        tduration = tduration % (24 * 3600)
        hour = int(tduration // 3600)
        tduration %= 3600
        minutes = int(tduration // 60)
        tduration %= 60
        seconds = int(tduration)
        retval = str(day)+"d"+str(hour)+"h"+str(minutes)+"m"+str(seconds)+"s"
    else:
        retval = "-"
    return retval


class ReportsPage(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'reports/reports_base.html'
    permission_required = ('invs.view_inv',)

class ReportsDashboardPage(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'reports/reports_dashboard.html'
    permission_required = ('invs.view_inv','tasks.view_task')

    def get_context_data(self, **kwargs):
        # check remaining session time
        session_key = self.request.COOKIES["sessionid"]
        session = Session.objects.get(session_key=session_key)
        sessiontimeout = session.expire_date
        servertime = datetime.now(timezone.utc)
        # check remaining session time

        kwargs['user'] = self.request.user
        # Closed investigations

        kwargs['invs_closed'] = Inv.objects.all()\
            .values('status__name')\
            .annotate(Count('status'))\
            .order_by('status__name')

        kwargs['invs_closed_30'] = Inv.objects.filter(created_at__gt=timezone_now()-timedelta(days=30))\
            .values('status__name')\
            .annotate(Count('status'))\
            .order_by('status__name')

        kwargs['invs_closed_90'] = Inv.objects.filter(created_at__gt=timezone_now()-timedelta(days=30))\
            .values('status__name')\
            .annotate(Count('status'))\
            .order_by('status__name')

        invduration_values = Inv.objects.all()\
            .filter(status=2)\
            .aggregate(Min('invduration'), Max('invduration'), Avg('invduration'))
        kwargs['invs_closed_stats_min'] = durationprint(invduration_values['invduration__min'])
        kwargs['invs_closed_stats_avg'] = durationprint(invduration_values['invduration__avg'])
        kwargs['invs_closed_stats_max'] = durationprint(invduration_values['invduration__max'])

        invduration_values_30 = Inv.objects.all()\
            .filter(status=2)\
            .aggregate(Min('invduration'), Max('invduration'), Avg('invduration'))
        kwargs['invs_closed_stats30_min'] = durationprint(invduration_values_30['invduration__min'])
        kwargs['invs_closed_stats30_avg'] = durationprint(invduration_values_30['invduration__avg'])
        kwargs['invs_closed_stats30_max'] = durationprint(invduration_values_30['invduration__max'])

        invduration_values_90 = Inv.objects.all()\
            .filter(status=2)\
            .aggregate(Min('invduration'), Max('invduration'), Avg('invduration'))
        kwargs['invs_closed_stats90_min'] = durationprint(invduration_values_90['invduration__min'])
        kwargs['invs_closed_stats90_avg'] = durationprint(invduration_values_90['invduration__avg'])
        kwargs['invs_closed_stats90_max'] = durationprint(invduration_values_90['invduration__max'])

        # tasks per inv
        inv_closed_tasks = Inv.objects.all()\
            .filter(created_at__gt=timezone_now()-timedelta(days=30))\
            .values('pk')\
            .annotate(Count('task_inv'))\
            .order_by('pk') \
            .aggregate(Min('task_inv__count'), Avg('task_inv__count'), Max('task_inv__count'))

        kwargs['invs_closed_tasks_min'] = int(inv_closed_tasks['task_inv__count__min'])
        kwargs['invs_closed_tasks_avg'] = round(inv_closed_tasks['task_inv__count__avg'])
        kwargs['invs_closed_tasks_max'] = int(inv_closed_tasks['task_inv__count__max'])

        inv_closed_tasks_manual = Inv.objects.filter(task_inv__type=2) \
            .filter(created_at__gt=timezone_now() - timedelta(days=30)) \
            .values('pk')\
            .annotate(Count('task_inv'))\
            .order_by('pk') \
            .aggregate(Min('task_inv__count'), Avg('task_inv__count'), Max('task_inv__count'))
        kwargs['invs_closed_tasks_manual_min'] = int(inv_closed_tasks_manual['task_inv__count__min'])
        kwargs['invs_closed_tasks_manual_avg'] = round(inv_closed_tasks_manual['task_inv__count__avg'])
        kwargs['invs_closed_tasks_manual_max'] = int(inv_closed_tasks_manual['task_inv__count__max'])

        inv_closed_tasks_auto = Inv.objects.filter(task_inv__type=1) \
            .filter(created_at__gt=timezone_now() - timedelta(days=30)) \
            .values('pk')\
            .annotate(Count('task_inv'))\
            .order_by('pk') \
            .aggregate(Min('task_inv__count'), Avg('task_inv__count'), Max('task_inv__count'))
        kwargs['invs_closed_tasks_auto_min'] = int(inv_closed_tasks_auto['task_inv__count__min'])
        kwargs['invs_closed_tasks_auto_avg'] = round(inv_closed_tasks_auto['task_inv__count__avg'])
        kwargs['invs_closed_tasks_auto_max'] = int(inv_closed_tasks_auto['task_inv__count__max'])
        #  Tasks
        kwargs['tasks_closed'] = Task.objects.all()\
            .values('status__name')\
            .annotate(Count('status'))\
            .order_by('status__name')

        kwargs['tasks_closed_30'] = Task.objects.all()\
            .filter(created_at__gt=timezone_now()-timedelta(days=30))\
            .values('status__name')\
            .annotate(Count('status'))\
            .order_by('status__name')

        kwargs['tasks_closed_90'] = Task.objects.all()\
            .filter(created_at__gt=timezone_now()-timedelta(days=30))\
            .values('status__name')\
            .annotate(Count('status'))\
            .order_by('status__name')

        taskduration_values = Task.objects.all()\
            .filter(status=2)\
            .aggregate(Min('taskduration'), Max('taskduration'), Avg('taskduration'))
        kwargs['tasks_closed_stats_min'] = durationprint(taskduration_values['taskduration__min'])
        kwargs['tasks_closed_stats_avg'] = durationprint(taskduration_values['taskduration__avg'])
        kwargs['tasks_closed_stats_max'] = durationprint(taskduration_values['taskduration__max'])

        taskduration_values_30 = Task.objects.all()\
            .filter(status=2)\
            .aggregate(Min('taskduration'), Max('taskduration'), Avg('taskduration'))
        kwargs['tasks_closed_stats30_min'] = durationprint(taskduration_values_30['taskduration__min'])
        kwargs['tasks_closed_stats30_avg'] = durationprint(taskduration_values_30['taskduration__avg'])
        kwargs['tasks_closed_stats30_max'] = durationprint(taskduration_values_30['taskduration__max'])

        taskduration_values_90 = Task.objects.all()\
            .filter(status=2)\
            .aggregate(Min('taskduration'), Max('taskduration'), Avg('taskduration'))
        kwargs['tasks_closed_stats90_min'] = durationprint(taskduration_values_90['taskduration__min'])
        kwargs['tasks_closed_stats90_avg'] = durationprint(taskduration_values_90['taskduration__avg'])
        kwargs['tasks_closed_stats90_max'] = durationprint(taskduration_values_90['taskduration__max'])

        return super(ReportsDashboardPage, self).get_context_data(**kwargs)



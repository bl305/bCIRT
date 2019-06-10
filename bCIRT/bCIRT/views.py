from django.views.generic import TemplateView
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from invs.models import Inv
from tasks.models import Task
# check remaining session time
from django.contrib.sessions.models import Session
from datetime import datetime, timezone
# check remaining session time
from django.contrib.auth import get_user_model
User = get_user_model()


class HomePage(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = "index.html"
    permission_required = ('invs.view_inv','tasks.view_task')

    def get_context_data(self, **kwargs):
        # check remaining session time
        session_key = self.request.COOKIES["sessionid"]
        session = Session.objects.get(session_key=session_key)
        sessiontimeout = session.expire_date
        servertime = datetime.now(timezone.utc)
        # print(sessiontimeout)
        # print(servertime)
        # c = servertime - sessiontimeout
        # print(divmod(c.days * 86400 + c.seconds, 60))

        # check remaining session time

        kwargs['user'] = self.request.user
        kwargs['invs'] = Inv.objects.filter(user=self.request.user, status=3)
        kwargs['uinvs'] = Inv.objects.exclude(status=3).exclude(status=2)
        kwargs['oinvs'] = Inv.objects.filter(status=3).exclude(user=self.request.user)
        kwargs['tasks'] = Task.objects.filter(user=self.request.user).exclude(status=2).exclude(type=1)
        kwargs['utasks'] = Task.objects.filter(status=1).exclude(type=1)
        kwargs['otasks'] = Task.objects.exclude(user=self.request.user).exclude(status=2).exclude(type=1)
        kwargs['rtasks'] = Task.objects.filter(user=self.request.user).order_by('-modified_at')[:5]
        return super(HomePage, self).get_context_data(**kwargs)




from .models import Inv, InvStatus
from tasks.models import TaskTemplate, PlaybookTemplate, Action
from .forms import InvForm
from django.shortcuts import redirect, reverse    # ,render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.views import generic
import logging
from django.utils.http import is_safe_url
from bCIRT.settings import ALLOWED_HOSTS, PROJECT_ROOT
# check remaining session time
from django.contrib.sessions.models import Session
from datetime import datetime, timezone
# check remaining session time
from django.template.loader import get_template
from django.http import HttpResponse
from weasyprint import HTML, CSS
from wkhtmltopdf.views import PDFTemplateResponse
from django.contrib.auth import get_user_model
User = get_user_model()
logger = logging.getLogger('log_file_verbose')


# Create your views here.
class MyPDFView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    # context = {"title": "Task evidences"}  # data that has to be rendered to pdf templete
    model = Inv
    permission_required = ('invs.view_inv', 'tasks.view_evidence', 'tasks:view_task', 'tasks:view_playbook')
    context = {"title": "Investigation evidences"}

    def get(self, request, *args, **kwargs):
        self.context['inv'] = self.get_object()
        self.context['user'] = self.request.user.get_username()

        html_template = get_template('invs/inv_detail_REPORT_v1.html')

        # rendered_html = html_template.render(self.context)
        #
        # css_path = custom_params.PROJECT_ROOT + '/static/bCIRT/bootstrap-3.3.7/css/bootstrap.min.css'
        # pdf_file = HTML(string=rendered_html).write_pdf(stylesheets=[CSS(css_path)])
        # # pdf_file = HTML(string=rendered_html).write_pdf()

        # http_response = HttpResponse(pdf_file, content_type='application/pdf')
        # http_response['Content-Disposition'] = 'filename="report_investigation.pdf"'
        response = PDFTemplateResponse(request=request,
                                       template=html_template,
                                       filename="investigation_report_" + str(self.get_object().pk) + ".pdf",
                                       context=self.context,
                                       show_content_in_browser=False,
                                       cmd_options={'margin-top': 10,
                                                    "zoom": 1,
                                                    "viewport-size": "1366 x 513",
                                                    'javascript-delay': 1000,
                                                    'footer-center': '[page]/[topage]',
                                                    "no-stop-slow-scripts": True},
                                       )

        return response


class MyPDFView_weasyprint(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):

    # context = {"title": "Task evidences"}  # data that has to be rendered to pdf templete
    model = Inv
    permission_required = ('invs.view_inv', 'tasks.view_evidence', 'tasks:view_task', 'tasks:view_playbook')
    context = {"title": "Investigation evidences"}

    def get(self, request, *args, **kwargs):
        self.context['inv'] = self.get_object()
        self.context['user'] = self.request.user.get_username()

        html_template = get_template('invs/inv_detail_REPORT.html')

        rendered_html = html_template.render(self.context)

        css_path = PROJECT_ROOT + '/static/bCIRT/bootstrap-3.3.7/css/bootstrap.min.css'
        pdf_file = HTML(string=rendered_html).write_pdf(stylesheets=[CSS(css_path)])
        # pdf_file = HTML(string=rendered_html).write_pdf()

        http_response = HttpResponse(pdf_file, content_type='application/pdf')
        http_response['Content-Disposition'] = 'filename="report_investigation.pdf"'

        return http_response


class InvDetailPrintView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = Inv
    template_name = 'invs/inv_detail_REPORT_v1.html'
    permission_required = ('invs.view_inv',)

    def get_context_data(self, **kwargs):
        # check remaining session time
        session_key = self.request.COOKIES["sessionid"]
        session = Session.objects.get(session_key=session_key)
        sessiontimeout = session.expire_date
        servertime = datetime.now(timezone.utc)
        # check remaining session time
        kwargs['templatecategories'] = TaskTemplate.objects.filter(enabled=True)
        kwargs['playbooks'] = PlaybookTemplate.objects.filter(enabled=True)
        kwargs['actions'] = Action.objects.filter(enabled=True)
        return super(InvDetailPrintView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('invs.view_inv'):
            messages.error(self.request, "No permission to view a record !!!")
            return redirect('invs:inv_list')
        # Checks pass, let http method handlers process the request
        return super(InvDetailPrintView, self).dispatch(request, *args, **kwargs)


# #############################################################################3
# Investigation related views
class InvListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Inv
    form_class = InvForm
    permission_required = ('invs.view_inv',)

    def get_context_data(self, **kwargs):
        # check remaining session time
        session_key = self.request.COOKIES["sessionid"]
        session = Session.objects.get(session_key=session_key)
        sessiontimeout = session.expire_date
        servertime = datetime.now(timezone.utc)
        # check remaining session time
        return super(InvListView, self).get_context_data(**kwargs)


class InvCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Inv
    form_class = InvForm
    permission_required = ('invs.add_inv',)
    success_url = 'invs:inv_list'

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        # check remaining session time
        session_key = self.request.COOKIES["sessionid"]
        session = Session.objects.get(session_key=session_key)
        sessiontimeout = session.expire_date
        servertime = datetime.now(timezone.utc)
        # check remaining session time
        return super(InvCreateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # self.object.user = self.request.user
        self.object.user = None
        self.object.modified_by = self.request.user.get_username()
        self.object.created_by = self.request.user.get_username()
        self.object.save()
        return super(InvCreateView, self).form_valid(form)

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
        return super(InvCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(InvCreateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        # kwargs['inv_pk'] = self.kwargs.get('inv_pk')
        kwargs['user'] = self.request.user
        return kwargs

class InvDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = Inv
    permission_required = ('invs.view_inv',)

    def get_context_data(self, **kwargs):
        # check remaining session time
        session_key = self.request.COOKIES["sessionid"]
        session = Session.objects.get(session_key=session_key)
        sessiontimeout = session.expire_date
        servertime = datetime.now(timezone.utc)
        # check remaining session time
        kwargs['templatecategories'] = TaskTemplate.objects.filter(enabled=True)
        kwargs['playbooks'] = PlaybookTemplate.objects.filter(enabled=True)
        kwargs['actions'] = Action.objects.filter(enabled=True)
        return super(InvDetailView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('invs.view_inv'):
            messages.error(self.request, "No permission to view a record !!!")
            return redirect('invs:inv_list')
        # Checks pass, let http method handlers process the request
        return super(InvDetailView, self).dispatch(request, *args, **kwargs)


class InvUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    login_url = '/'
    redirect_field_name = 'invs/inv_detail.html'
    form_class = InvForm
    model = Inv
    permission_required = ('invs.change_inv',)
    success_url = 'invs:inv_list'

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        # check remaining session time
        session_key = self.request.COOKIES["sessionid"]
        session = Session.objects.get(session_key=session_key)
        sessiontimeout = session.expire_date
        servertime = datetime.now(timezone.utc)
        # check remaining session time
        return super(InvUpdateView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('invs.change_inv'):
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('invs:inv_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(InvUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.modified_by = self.request.user.get_username()
        self.object.save()
        return super(InvUpdateView, self).form_valid(form)


class InvRemoveView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Inv
    permission_required = ('invs.delete_inv',)
    success_url = 'invs:inv_list'

    def get_success_url(self):
        return reverse(self.success_url)

    def get_context_data(self, **kwargs):
        # check remaining session time
        session_key = self.request.COOKIES["sessionid"]
        session = Session.objects.get(session_key=session_key)
        sessiontimeout = session.expire_date
        servertime = datetime.now(timezone.utc)
        # check remaining session time
        return super(InvRemoveView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('invs.delete_inv'):
            messages.error(self.request, "No permission to delete a record !!!")
            return redirect('invs:inv_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(InvRemoveView, self).dispatch(request, *args, **kwargs)


class InvAssignView(LoginRequiredMixin, PermissionRequiredMixin, generic.RedirectView):
    permission_required = ('invs.view_inv', 'invs.change_inv')
    success_url = 'invs:inv_list'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('invs.change_inv'):
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('invs:inv_list')
        inv_pk = self.kwargs.get('pk')
        # Checks pass, let http method handlers process the request
        Inv.objects.filter(pk=inv_pk).update(user=self.request.user)
        assigned_pk = InvStatus.objects.get(name='Assigned')
        Inv.objects.filter(pk=inv_pk).update(status=assigned_pk)
        # return redirect(self.success_url)
        return super(InvAssignView, self).dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to
        # return reverse('tasks:tsk_list')
        # return super().get_redirect_url(*args, **kwargs)

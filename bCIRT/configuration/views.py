from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from .models import UpdatePackage
from django.utils.http import is_safe_url
from django.shortcuts import reverse, redirect
from bCIRT import custom_params
from django.contrib.sessions.models import Session
from datetime import datetime, timezone
from django.contrib import messages
from .forms import UpdatePackageForm
# Create your views here.

import logging
logger = logging.getLogger('log_file_verbose')


class ConfigurationPage(LoginRequiredMixin, TemplateView):
    template_name = 'configuration/configuration_base.html'


class ConfigurationLoggingPage(LoginRequiredMixin, TemplateView):
    template_name = 'configuration/configuration_logging.html'


class UpdatePackageListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = UpdatePackage
    form_class = UpdatePackageForm
    permission_required = ('configuration.view_updatepackage',)

    def get_context_data(self, **kwargs):
        # check remaining session time
        session_key = self.request.COOKIES["sessionid"]
        session = Session.objects.get(session_key=session_key)
        sessiontimeout = session.expire_date
        servertime = datetime.now(timezone.utc)
        return super(UpdatePackageListView, self).get_context_data(**kwargs)


class UpdatePackageCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = UpdatePackage
    form_class = UpdatePackageForm
    permission_required = ('configuration.add_updatepackage',)
    success_url = 'configuration:conf_base'

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=custom_params.ALLOWED_HOSTS):
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

        return super(UpdatePackageCreateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.modified_by = self.request.user.get_username()
        self.object.created_by = self.request.user.get_username()
        if self.request.FILES:
            self.object.fileName = self.request.FILES['fileRef'].name
        self.object.save()
        return super(UpdatePackageCreateView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.add_evidence'):
            messages.error(self.request, "No permission to add a record !!!")
            return redirect('configuration:conf_updatelist')
        # Checks pass, let http method handlers process the request
        return super(UpdatePackageCreateView, self).dispatch(request, *args, **kwargs)


class UpdatePackageDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = UpdatePackage
    permission_required = ('configuration.view_updatepackage',)

    def get_context_data(self, **kwargs):
        # check remaining session time
        session_key = self.request.COOKIES["sessionid"]
        session = Session.objects.get(session_key=session_key)
        sessiontimeout = session.expire_date
        servertime = datetime.now(timezone.utc)
        # check remaining session time
        return super(UpdatePackageDetailView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('configuration.view_updatepackage'):
            messages.error(self.request, "No permission to view a record !!!")
            return redirect('configuration:conf_updatedetail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(UpdatePackageDetailView, self).dispatch(request, *args, **kwargs)


class UpdatePackageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/'
    form_class = UpdatePackageForm
    model = UpdatePackage
    permission_required = ('configuration.change_updatepackage',)
    success_url = 'configuration:conf_updatelist'

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=custom_params.ALLOWED_HOSTS):
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
        return super(UpdatePackageUpdateView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('configuration.change_updatepackage'):
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('configuration:conf_updatedetail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(UpdatePackageUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.modified_by = self.request.user.get_username()
        if self.request.FILES:
            self.object.fileName = self.request.FILES['fileRef'].name
        self.object.save()
        return super(UpdatePackageUpdateView, self).form_valid(form)

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(UpdatePackageUpdateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        kwargs['user'] = self.request.user
        # inv_pk = self.kwargs.get('inv_pk')
        return kwargs


class UpdatePackageRemoveView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = UpdatePackage
    permission_required = ('configuration.delete_updatepackage', 'configuration.view_updatepackage',)
    success_url = 'configuration:ev_list'

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=custom_params.ALLOWED_HOSTS):
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
        return super(UpdatePackageRemoveView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('configuration.delete_updatepackage'):
            messages.error(self.request, "No permission to delete a record !!!")
            return redirect('configuration:ev_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(UpdatePackageRemoveView, self).dispatch(request, *args, **kwargs)

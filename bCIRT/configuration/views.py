# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : configuration/views.py
# Author            : Balazs Lendvay
# Date created      : 2019.07.27
# Purpose           : View file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.07.29  Lendvay     1      Initial file
# 2019.09.06  Lendvay     2      Added session security
# **********************************************************************;
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import UpdatePackage, ConnectionItem, ConnectionItemField
from django.views import generic
from django.utils.http import is_safe_url
from django.shortcuts import reverse, redirect
from bCIRT.settings import ALLOWED_HOSTS
# from django.contrib.sessions.models import Session
# from datetime import datetime, timezone
from django.contrib import messages
from .forms import UpdatePackageForm, ConnectionItemForm, ConnectionItemFieldForm
# Create your views here.
from os import path
from bCIRT.custom_variables import LOGLEVEL, LOGSEPARATOR
import logging
logger = logging.getLogger('log_file_verbose')


class ConfigurationPage(LoginRequiredMixin, TemplateView):
    template_name = 'configuration/configuration_base.html'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(ConfigurationPage, self).__init__(*args, **kwargs)


class ConfigurationLoggingPage(LoginRequiredMixin, TemplateView):
    template_name = 'configuration/configuration_logging.html'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(ConfigurationLoggingPage, self).__init__(*args, **kwargs)


class ConfigurationAboutPage(LoginRequiredMixin, TemplateView):
    template_name = 'configuration/configuration_about.html'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(ConfigurationAboutPage, self).__init__(*args, **kwargs)


class UpdatePackageListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = UpdatePackage
    form_class = UpdatePackageForm
    permission_required = ('configuration.view_updatepackage',)

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(UpdatePackageListView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        return super(UpdatePackageListView, self).get_context_data(**kwargs)


@method_decorator(csrf_exempt, name='dispatch')
class UpdatePackageCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = UpdatePackage
    form_class = UpdatePackageForm
    permission_required = ('configuration.add_updatepackage',)
    success_url = 'configuration:conf_updatelist'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(UpdatePackageCreateView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
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
        elif not self.request.user.has_perm('configuration.add_evidence'):
            messages.error(self.request, "No permission to add a record !!!")
            return redirect('configuration:conf_updatelist')
        # Checks pass, let http method handlers process the request
        return super(UpdatePackageCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(UpdatePackageCreateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        # kwargs['inv_pk'] = self.kwargs.get('inv_pk')
        kwargs['user'] = self.request.user
        return kwargs


class UpdatePackageDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = UpdatePackage
    permission_required = ('configuration.view_updatepackage',)

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(UpdatePackageDetailView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
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


@method_decorator(csrf_exempt, name='dispatch')
class UpdatePackageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/'
    form_class = UpdatePackageForm
    model = UpdatePackage
    permission_required = ('configuration.view_updatepackage', 'configuration.change_updatepackage',)
    success_url = 'configuration:conf_updatelist'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(UpdatePackageUpdateView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
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
    success_url = 'configuration:conf_updatelist'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(UpdatePackageRemoveView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(UpdatePackageRemoveView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('configuration.delete_updatepackage'):
            messages.error(self.request, "No permission to delete a record !!!")
            return redirect('configuration:conf_updatedetail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(UpdatePackageRemoveView, self).dispatch(request, *args, **kwargs)


class InstallPackageRedirectView(LoginRequiredMixin, PermissionRequiredMixin, generic.RedirectView):
    """
    This class performs the "action" execution and records the output in the ActionQ table.
    """
    permission_required = ('configuration.view_updatepackage', 'configuration.change_updatepackage')
    success_url = 'configuration:conf_updatelist'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(InstallPackageRedirectView, self).__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('configuration.view_updatepackage'):
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('configuration:conf_updatelist')
        else:
            from bCIRT.settings import PROJECT_ROOT, MEDIA_ROOT
            p_root = PROJECT_ROOT.rstrip('//')
            p_path = path.dirname(p_root)
            conf_obj = UpdatePackage.objects.get(pk=self.kwargs.get('pk'))
            if conf_obj.fileRef:
                update_file = path.join(MEDIA_ROOT, str(conf_obj.fileRef))
                import zipfile
                with zipfile.ZipFile(update_file, "r") as zip_ref:
                    zip_ref.extractall(p_path)

        return super(InstallPackageRedirectView, self).dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to
        # return reverse('configuration:actq_detail', kwargs={'pk': self.actq})
        # return reverse('configuration:act_list')
        # return super().get_redirect_url(*args, **kwargs)


class ConnectionItemListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = ConnectionItem
    form_class = ConnectionItemForm
    permission_required = ('configuration.view_connectionitem',)

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(ConnectionItemListView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        return super(ConnectionItemListView, self).get_context_data(**kwargs)


class ConnectionItemCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    #  fields = ("inv", "user", "description", "fileRef")
    model = ConnectionItem
    form_class = ConnectionItemForm
    permission_required = ('configuration.add_connectionitem',)
    success_url = 'configuration:connitem_list'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(ConnectionItemCreateView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(ConnectionItemCreateView, self).get_context_data(**kwargs)

    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     self.object.save()
    #     return super(ConnectionItemCreateView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('configuration.add_connectionitem'):
            messages.error(self.request, "No permission to add a record !!!")
            return redirect('configuration:connitem_list')
        # Checks pass, let http method handlers process the request
        return super(ConnectionItemCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        # grab the current set of form #kwargs
        kwargs = super(ConnectionItemCreateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        kwargs['user'] = self.request.user
        return kwargs


class ConnectionItemDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = ConnectionItem
    permission_required = ('configuration.view_connectionitem',)

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(ConnectionItemDetailView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        return super(ConnectionItemDetailView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('configuration.view_connectionitem'):
            messages.error(self.request, "No permission to view a record !!!")
            return redirect('configuration:connitem_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(ConnectionItemDetailView, self).dispatch(request, *args, **kwargs)


class ConnectionItemUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    login_url = '/'
    # redirect_field_name = 'tasks/evidence_detail.html'
    form_class = ConnectionItemForm
    model = ConnectionItem
    permission_required = ('configuration.change_connectionitem',)
    success_url = 'configuration:connitem_list'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(ConnectionItemUpdateView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(ConnectionItemUpdateView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('configuration.change_connectionitem'):
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('configuration:connitem_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(ConnectionItemUpdateView, self).dispatch(request, *args, **kwargs)

    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     self.object.save()
    #     return super(ConnectionItemUpdateView, self).form_valid(form)

    def get_form_kwargs(self):
        # grab the current set of form #kwargs
        kwargs = super(ConnectionItemUpdateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        kwargs['user'] = self.request.user
        return kwargs


class ConnectionItemRemoveView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = ConnectionItem
#    success_url = reverse_lazy('configuration:ev_list')
    permission_required = ('configuration.delete_connectionitem', 'configuration.view_connectionitem',)
    success_url = 'configuration:connitem_list'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(ConnectionItemRemoveView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(ConnectionItemRemoveView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('configuration.delete_connectionitem'):
            messages.error(self.request, "No permission to delete a record !!!")
            return redirect('configuration:connitem_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(ConnectionItemRemoveView, self).dispatch(request, *args, **kwargs)

# ConnectionItemFields


class ConnectionItemFieldListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = ConnectionItemField
    form_class = ConnectionItemFieldForm
    permission_required = ('configuration.view_connectionitemfield',)

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(ConnectionItemFieldListView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        return super(ConnectionItemFieldListView, self).get_context_data(**kwargs)


class ConnectionItemFieldCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    #  fields = ("inv", "user", "description", "fileRef")
    model = ConnectionItemField
    form_class = ConnectionItemFieldForm
    permission_required = ('configuration.add_connectionitemfield',)
    success_url = 'configuration:connitemf_list'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(ConnectionItemFieldCreateView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(ConnectionItemFieldCreateView, self).get_context_data(**kwargs)

    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     self.object.save()
    #     return super(ConnectionItemCreateView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('configuration.add_connectionitemfield'):
            messages.error(self.request, "No permission to add a record !!!")
            return redirect('configuration:connitemf_list')
        # Checks pass, let http method handlers process the request
        return super(ConnectionItemFieldCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        # grab the current set of form #kwargs
        kwargs = super(ConnectionItemFieldCreateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        kwargs['user'] = self.request.user
        return kwargs


class ConnectionItemFieldDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = ConnectionItemField
    permission_required = ('configuration.view_connectionitemfield',)

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(ConnectionItemFieldDetailView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        return super(ConnectionItemFieldDetailView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('configuration.view_connectionitemfield'):
            messages.error(self.request, "No permission to view a record !!!")
            return redirect('configuration:connitemf_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(ConnectionItemFieldDetailView, self).dispatch(request, *args, **kwargs)


class ConnectionItemFieldUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    login_url = '/'
    # redirect_field_name = 'tasks/evidence_detail.html'
    form_class = ConnectionItemFieldForm
    model = ConnectionItemField
    permission_required = ('configuration.change_connectionitemfield',)
    success_url = 'configuration:connitemf_list'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(ConnectionItemFieldUpdateView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(ConnectionItemFieldUpdateView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('configuration.change_connectionitemfield'):
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('configuration:connitemf_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(ConnectionItemFieldUpdateView, self).dispatch(request, *args, **kwargs)

    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     self.object.save()
    #     return super(ConnectionItemUpdateView, self).form_valid(form)

    def get_form_kwargs(self):
        # grab the current set of form #kwargs
        kwargs = super(ConnectionItemFieldUpdateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        kwargs['user'] = self.request.user
        return kwargs


class ConnectionItemFieldRemoveView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = ConnectionItemField
#    success_url = reverse_lazy('configuration:ev_list')
    permission_required = ('configuration.delete_connectionitem', 'configuration.view_connectionitemfield',)
    success_url = 'configuration:connitemf_list'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(ConnectionItemFieldRemoveView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(ConnectionItemFieldRemoveView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('configuration.delete_connectionitemfield'):
            messages.error(self.request, "No permission to delete a record !!!")
            return redirect('configuration:connitemf_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(ConnectionItemFieldRemoveView, self).dispatch(request, *args, **kwargs)

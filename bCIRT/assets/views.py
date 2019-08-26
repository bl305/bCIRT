# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : assets/views.py
# Author            : Balazs Lendvay
# Date created      : 2019.07.27
# Purpose           : View file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.07.29  Lendvay     1      Initial file
# **********************************************************************;
# from django.shortcuts import render
from .models import Host, Profile, new_profile
from .forms import HostForm, ProfileForm
from tasks.models import EvidenceAttr
from invs.models import Inv
from django.shortcuts import redirect, reverse  # ,render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.views import generic
import logging
from bCIRT.custom_variables import LOGSEPARATOR, LOGLEVEL
from django.utils.http import is_safe_url
from bCIRT.settings import ALLOWED_HOSTS
# check remaining session time
from django.contrib.sessions.models import Session
from datetime import datetime, timezone
# check remaining session time
from django.contrib.auth import get_user_model
User = get_user_model()

logger = logging.getLogger('log_file_verbose')

# Create your views here.
# #############################################################################3
# Investigation related views
class HostListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Host
    form_class = HostForm
    permission_required = ('assets.view_host',)

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR +"call"+LOGSEPARATOR+self.__class__.__name__
            logger.info(logmsg)
        super(HostListView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # check remaining session time
        session_key = self.request.COOKIES["sessionid"]
        session = Session.objects.get(session_key=session_key)

        sessiontimeout = session.expire_date
        servertime = datetime.now(timezone.utc)
        # check remaining session time
        return super(HostListView, self).get_context_data(**kwargs)


class HostCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Host
    form_class = HostForm
    permission_required = ('assets.add_host',)
    success_url = 'assets:host_list'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR +"call"+LOGSEPARATOR+self.__class__.__name__
            logger.info(logmsg)
        super(HostCreateView, self).__init__(*args, **kwargs)

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
        return super(HostCreateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.modified_by = self.request.user.get_username()
        self.object.created_by = self.request.user.get_username()
        self.object.save()
        return super(HostCreateView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('assets.add_host'):
            messages.error(self.request, "No permission to add a record !!!")
            return redirect('assets:host_list')
        # Checks pass, let http method handlers process the request
        return super(HostCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(HostCreateView, self).get_form_kwargs()
        return kwargs


class HostDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = Host
    permission_required = ('assets.view_host',)

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR +"call"+LOGSEPARATOR+self.__class__.__name__
            logger.info(logmsg)
        super(HostDetailView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # check remaining session time
        session_key = self.request.COOKIES["sessionid"]
        session = Session.objects.get(session_key=session_key)

        sessiontimeout = session.expire_date
        servertime = datetime.now(timezone.utc)
        # check remaining session time
        return super(HostDetailView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('assets.view_host'):
            messages.error(self.request, "No permission to view a record !!!")
            return redirect('assets:host_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(HostDetailView, self).dispatch(request, *args, **kwargs)


class HostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    login_url = '/'
    form_class = HostForm
    model = Host
    permission_required = ('assets.change_host',)
    success_url = 'assets:host_list'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR +"call"+LOGSEPARATOR+self.__class__.__name__
            logger.info(logmsg)
        super(HostUpdateView, self).__init__(*args, **kwargs)

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
        return super(HostUpdateView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('assets.change_host'):
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('assets:host_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(HostUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.modified_by = self.request.user.get_username()
        self.object.save()
        return super(HostUpdateView, self).form_valid(form)

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(HostUpdateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        # kwargs['user'] = self.request.user
        return kwargs


class HostRemoveView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Host
    permission_required = ('assets.delete_host', 'assets.view_host',)
    success_url = 'assets:host_list'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR +"call"+LOGSEPARATOR+self.__class__.__name__
            logger.info(logmsg)
        super(HostRemoveView, self).__init__(*args, **kwargs)

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
        return super(HostRemoveView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('assets.delete_host'):
            messages.error(self.request, "No permission to delete a record !!!")
            return redirect('assets:host_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(HostRemoveView, self).dispatch(request, *args, **kwargs)


# ################# PROFILE
# Create your views here.
# #############################################################################3
# Investigation related views
class ProfileListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Profile
    form_class = ProfileForm
    permission_required = ('assets.view_profile',)

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR +"call"+LOGSEPARATOR+self.__class__.__name__
            logger.info(logmsg)
        super(ProfileListView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # check remaining session time
        session_key = self.request.COOKIES["sessionid"]
        session = Session.objects.get(session_key=session_key)
        sessiontimeout = session.expire_date
        servertime = datetime.now(timezone.utc)
        # check remaining session time
        return super(ProfileListView, self).get_context_data(**kwargs)


class ProfileCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Profile
    form_class = ProfileForm
    permission_required = ('assets.add_profile',)
    success_url = 'assets:prof_list'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR +"call"+LOGSEPARATOR+self.__class__.__name__
            logger.info(logmsg)
        super(ProfileCreateView, self).__init__(*args, **kwargs)

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
        return super(ProfileCreateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.modified_by = self.request.user.get_username()
        self.object.created_by = self.request.user.get_username()
        self.object.save()
        return super(ProfileCreateView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('assets.add_profile'):
            messages.error(self.request, "No permission to add a record !!!")
            return redirect('assets:prof_list')
        # Checks pass, let http method handlers process the request
        return super(ProfileCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(ProfileCreateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        inv_pk = self.kwargs.get('inv_pk')
        if inv_pk:
            pass
        else:
            inv_pk = 0
        kwargs['inv_pk'] = inv_pk
        return kwargs


class ProfileDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = Profile
    permission_required = ('assets.view_profile',)

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR +"call"+LOGSEPARATOR+self.__class__.__name__
            logger.info(logmsg)
        super(ProfileDetailView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # check remaining session time
        session_key = self.request.COOKIES["sessionid"]
        session = Session.objects.get(session_key=session_key)

        sessiontimeout = session.expire_date
        servertime = datetime.now(timezone.utc)
        # check remaining session time
        return super(ProfileDetailView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('assets.view_profile'):
            messages.error(self.request, "No permission to view a record !!!")
            return redirect('assets:prof_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(ProfileDetailView, self).dispatch(request, *args, **kwargs)


class ProfileUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    login_url = '/'
    form_class = ProfileForm
    model = Profile
    permission_required = ('assets.change_profile',)
    success_url = 'assets:prof_list'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR +"call"+LOGSEPARATOR+self.__class__.__name__
            logger.info(logmsg)
        super(ProfileUpdateView, self).__init__(*args, **kwargs)

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
        return super(ProfileUpdateView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('assets.change_profile'):
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('assets:prof_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(ProfileUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.modified_by = self.request.user.get_username()
        self.object.save()
        return super(ProfileUpdateView, self).form_valid(form)

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(ProfileUpdateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        # kwargs['user'] = self.request.user
        return kwargs


class ProfileRemoveView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Profile
#    success_url = reverse_lazy('tasks:ev_list')
    permission_required = ('assets.delete_profile', 'assets.view_profile',)
    success_url = 'assets:prof_list'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR +"call"+LOGSEPARATOR+self.__class__.__name__
            logger.info(logmsg)
        super(ProfileRemoveView, self).__init__(*args, **kwargs)

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
        return super(ProfileRemoveView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('assets.delete_profile'):
            messages.error(self.request, "No permission to delete a record !!!")
            return redirect('assets:prof_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(ProfileRemoveView, self).dispatch(request, *args, **kwargs)


class ProfileCreateRedirectView(LoginRequiredMixin, PermissionRequiredMixin, generic.RedirectView):
    """
    This class performs the "action" execution and records the output in the ActionQ table.
    """
    permission_required = ('assets.view_profile', 'assets.change_profile')
    success_url = 'assets:asset_list'
    actq = ""

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR +"call"+LOGSEPARATOR+self.__class__.__name__
            logger.info(logmsg)
        super(ProfileCreateRedirectView, self).__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('assets.change_profile'):
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('assets:profile_list')
        # Creating a new profile based on the attribute calling this function
        invpk = int(self.kwargs.get('inv_pk'))
        invobj = Inv.objects.get(pk=invpk)
        evattrpk = int(self.kwargs.get('evattr_pk'))
        evattr_obj = EvidenceAttr.objects.get(pk=evattrpk)
        evpk = int(self.kwargs.get('ev_pk'))
        # print("invpk:%s"%(invpk))
        # print("invobj:%s" % (invobj))
        # print("evattrpk:%s" % (evattrpk))
        # print("evattrobj:%s" % (evattr_obj))
        # print("evpk:%s" % (evpk))
        attrpklist = list()
        # if ev_pk=0, it is only one attribute to deal with
        if evpk == 0:
            attrpklist.append(evattr_obj)
            # print("attrpklist:%s" % (attrpklist))
        else:
            attributes = EvidenceAttr.objects.filter(ev__pk=evpk)
            # print("Attributes:%s"%(attributes))
            if attributes:
                for attritem in attributes:
                    attrpklist.append(attritem)
        # print("Attrpklist:%s"%(attrpklist))
        # print(type(attrpklist))
        for evattrobj in attrpklist:
            # find attributes and run the commands on them
            # if ev_pk is not 0, then we need to run it on all evidence attributes
            # evattrobj = EvidenceAttr.objects.get(pk=evattrpk)
            evattrtype = evattrobj.evattrformat.name
            ausername = None
            auserid = None
            aemail = None
            ahostname = None
            aip = None
            if evattrtype == "UserName":
                ausername = evattrobj.evattrvalue
            elif evattrtype == "UserID":
                auserid = evattrobj.evattrvalue
            elif evattrtype == "Email":
                aemail = evattrobj.evattrvalue
            elif evattrtype == "HostName":
                ahostname = evattrobj.evattrvalue
            elif evattrtype == "IPv4" or evattrtype == "IPv6":
                aip = evattrobj.evattrvalue
            else:
                pass

            # evattrvalue = evattrobj.evattrvalue
            new_profile(
                pinv=invobj,
                pusername=ausername,
                puserid=auserid,
                pemail=aemail,
                phost=ahostname,
                pip=aip,
                plocation=None,
                pdepartment=None,
                plocation_contact=None,
                pcreated_by=self.request.user.get_username(),
                pmodified_by=self.request.user.get_username(),
                pdescription="",
            )

        return super(ProfileCreateRedirectView, self).dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to
        # return reverse('tasks:actq_detail', kwargs={'pk': self.actq})

        # return reverse('tasks:act_list')
        # return super().get_redirect_url(*args, **kwargs)

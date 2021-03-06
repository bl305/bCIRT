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
# 2019.09.06  Lendvay     2      Added session security
# **********************************************************************;
# from django.shortcuts import render
from .models import Host, Profile, new_create_profile_from_evattrs
from .forms import HostForm, ProfileForm
# from tasks.models import EvidenceAttr
# from invs.models import Inv
from django.shortcuts import redirect, reverse, get_object_or_404  # ,render,
from django.http import JsonResponse
from django.template.loader import render_to_string

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
from django.db.models import Q

# check remaining session time
# from django.contrib.sessions.models import Session
# from datetime import datetime, timezone
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
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(HostListView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        return super(HostListView, self).get_context_data(**kwargs)


class HostCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Host
    form_class = HostForm
    permission_required = ('assets.add_host',)
    success_url = 'assets:host_list'

    def __init__(self, *args, **kwargs):
        self.object = None
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
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
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(HostDetailView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
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
        self.object = None
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
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
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
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
    # model = Profile
    # form_class = ProfileForm
    # permission_required = ('assets.view_profile',)
    #
    # def __init__(self, *args, **kwargs):
    #     if LOGLEVEL == 1:
    #         pass
    #     elif LOGLEVEL == 2:
    #         pass
    #     elif LOGLEVEL == 3:
    #         logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
    #         logger.info(logmsg)
    #     super(ProfileListView, self).__init__(*args, **kwargs)
    #
    # def get_context_data(self, **kwargs):
    #
    #     return super(ProfileListView, self).get_context_data(**kwargs)
    model = Profile
    form_class = ProfileForm
    permission_required = ('assets.view_profile',)
    paginate_by = 25

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(ProfileListView, self).__init__(*args, **kwargs)

    def get_queryset(self):
        result = super(ProfileListView, self).get_queryset()
        # search related stuff
        pager_raw = self.request.GET.get("pager")
        if pager_raw == "25":
            self.paginate_by = 25
        elif pager_raw == "50":
            self.paginate_by = 50
        elif pager_raw == "100":
            self.paginate_by = 100
        order_by = self.request.GET.get("order")
        if order_by == "id":
            order_by = "id"
        elif order_by == "created":
            order_by = "created_at"
        elif order_by == "modified":
            order_by = "modified_at"
        elif order_by == "username":
            order_by = "username"
        elif order_by == "userid":
            order_by = "userid"
        elif order_by == "email":
            order_by = "email"
        elif order_by == "host":
            order_by = "host"
        elif order_by == "ip":
            order_by = "ip"
        elif order_by == "location":
            order_by = "location"
        elif order_by == "department":
            order_by = "department"
        elif order_by == "location_contact":
            order_by = "location_contact"
        elif order_by == "investigation":
            order_by = "inv__pk"
        elif order_by == "description":
            order_by = "description"
        else:
            order_by = "id"
        queryset_list = Profile.objects.all().order_by(order_by)
        result = queryset_list
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                    Q(pk__icontains=query) |
                    Q(modified_by__icontains=query) |
                    Q(description__icontains=query) |
                    Q(created_by__icontains=query) |
                    Q(username__icontains=query) |
                    Q(userid__icontains=query) |
                    Q(email__icontains=query) |
                    Q(host__icontains=query) |
                    Q(ip__icontains=query) |
                    Q(location__icontains=query) |
                    Q(department__icontains=query) |
                    Q(location_contact__icontains=query) |
                    Q(inv__pk__icontains=query) |
                    Q(created_at__icontains=query) |
                    Q(modified_at__icontains=query) |
                    Q(description__icontains=query)
                    ).distinct().order_by(order_by)
            result = queryset_list
        return result

    def get_context_data(self, **kwargs):
        kwargs['pager'] = self.paginate_by
        itemnum = Profile.objects.all().count()
        divresult = divmod(itemnum, self.paginate_by)
        if divresult[1]:
            finres = divresult[0] + 1
        else:
            finres = 0
        kwargs['allcount'] = finres
        if self.request.GET.get('q'):
            kwargs['q'] = str(self.request.GET.get('q'))
        if self.request.GET.get('page'):
            kwargs['page'] = int(self.request.GET.get('page'))
        if self.request.GET.get('order'):
            kwargs['order'] = str(self.request.GET.get('order'))

        context = super(ProfileListView, self).get_context_data(**kwargs)
        return context

class ProfileCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Profile
    form_class = ProfileForm
    permission_required = ('assets.add_profile',)
    success_url = 'assets:prof_list'

    def __init__(self, *args, **kwargs):
        self.object = None
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
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
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(ProfileDetailView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
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
        self.object = None
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
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
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
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
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(ProfileCreateRedirectView, self).__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('assets.change_profile'):
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('assets:profile_list')
        ainv_pk = int(self.kwargs.get('inv_pk'))
        aevattr_pk = int(self.kwargs.get('evattr_pk'))
        aev_pk = int(self.kwargs.get('ev_pk'))
        ausername = self.request.user.get_username()
        new_create_profile_from_evattrs(pinv_pk=ainv_pk, pevattr_pk=aevattr_pk, pev_pk=aev_pk, pusername=ausername)
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


# ######## AJAX CRUD TEST
# from django.shortcuts import render

# def hosts_list(request):
#     hosts = Host.objects.all()
#     return render(request, 'assets/hosts_list.html', {'hosts': hosts})
# class HostListViewAjaxRaw(generic.View):
#     def get(self, request):
#         hosts =  list(Host.objects.all().values())
#         data =  dict()
#         data['hosts'] = hosts
#         return JsonResponse(data)

# def hosts_create(request):
#     form = HostForm()
#     context = {'form': form}
#     html_form = render_to_string('assets/partial_host_create.html',
#         context,
#         request=request,
#     )
#     return JsonResponse({'html_form': html_form})
#
def save_host_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            hosts = Host.objects.all()
            # data['html_data_list'] = render_to_string('assets/partial_host_list.html', {
            #     'hosts': hosts
            # })
            data['html_data_list'] = render_to_string('assets/host_list_tablebody.html', {
                'object_list': hosts
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def hostaj_create_view(request):
    if request.method == 'POST':
        form = HostForm(request.POST)
    else:
        form = HostForm()
    return save_host_form(request, form, 'assets/host_form_create_ajax.html')


def hostaj_update_view(request, pk):
    host = get_object_or_404(Host, pk=pk)
    if request.method == 'POST':
        form = HostForm(request.POST, instance=host)
    else:
        form = HostForm(instance=host)
    return save_host_form(request, form, 'assets/host_form_update_ajax.html')


def hostaj_delete_view(request, pk):
    host = get_object_or_404(Host, pk=pk)
    data = dict()
    if request.method == 'POST':
        host.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        hosts = Host.objects.all()
        data['html_data_list'] = render_to_string('assets/host_list_tablebody.html', {
            'object_list': hosts
        })
    else:
        context = {'host': host}
        data['html_form'] = render_to_string('assets/host_form_delete_ajax.html', context, request=request)
    return JsonResponse(data)

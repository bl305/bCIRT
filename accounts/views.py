# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : accounts/views.py
# Author            : Balazs Lendvay
# Date created      : 2019.07.27
# Purpose           : View file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.07.29  Lendvay     1      Initial file
# 2019.09.06  Lendvay     2      Added session security
# **********************************************************************;
from __future__ import unicode_literals
# password change imports
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from .models import UserAudit
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
# password change imports
from django.utils.timezone import now as timezone_now
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.dispatch import receiver
from django.db.models.signals import pre_save
# from django.contrib.auth.models import User
from . import forms
from django.contrib.auth import get_user_model
User = get_user_model()
from bCIRT.custom_variables import LOGLEVEL, LOGSEPARATOR
import logging
logger = logging.getLogger('log_file_verbose')


# Create your views here.
class RegisterAccountPage(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "accounts/account_register.html"

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(RegisterAccountPage, self).__init__(*args, **kwargs)


@receiver(pre_save, sender=User)
def set_new_user_inactive(sender, instance, **kwargs):
    # This is to disable newly created users
    if instance._state.adding is True:
        # print("Creating Inactive User")
        instance.is_active = True
        # enable the one below to disable users upon creation
        # this includes the first admin account!!!
        # instance.is_active = False
    else:
        # print("Updating User Record")
        pass


from users.models import Profile
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            profile_obj = Profile.objects.get(user__pk=request.user.pk)
            profile_obj.passwordmodified_at = timezone_now()
            profile_obj.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/account_change_password.html', {
        'form': form
    })


class UserAuditListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = UserAudit
    permission_required = ('configuration.view_useraudit',)

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(UserAuditListView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        return super(UserAuditListView, self).get_context_data(**kwargs)

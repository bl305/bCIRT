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

from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from . import forms
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
        print("Creating Inactive User")
        instance.is_active = True
        # enable the one below to disable users upon creation
        # this includes the first admin account!!!
        # instance.is_active = False
    else:
        print("Updating User Record")

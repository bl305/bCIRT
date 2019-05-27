# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from . import forms

# Create your views here.
class RegisterAccountPage(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "accounts/account_register.html"


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

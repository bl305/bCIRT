# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : assets/forms.py
# Author            : Balazs Lendvay
# Date created      : 2019.07.27
# Purpose           : Forms file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.07.29  Lendvay     1      Initial file
# **********************************************************************;
# from django.shortcuts import render
from django import forms
from .models import Host, Hostname, Ipaddress, Profile
from invs.models import Inv
import logging
from tinymce import TinyMCE
logger = logging.getLogger('log_file_verbose')


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class HostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(HostForm, self).__init__(*args, **kwargs)
        logger.info("HostFormCall - ")

    class Meta:
        fields = ("name", "description")
        model = Host
        labels = {
            "name": "Hostname*",
            "description": "Description",
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'size': 30,
                'style': 'width:50%',
                'class': 'form-control'}
            ),
            'description': TinyMCEWidget(
                mce_attrs={
                    'width': '90%',
                },
                attrs={
                    'style': 'padding-right: 100px',
                }
            ),
        }


class HostnameForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        super(HostnameForm, self).__init__(*args, **kwargs)
        logger.info("HostnameForm - ")

    class Meta:
        fields = ("name", "description", "hosts")
        model = Hostname
        labels = {
            "name": "Hostname",
            "description": "Description",
            "hosts": "Assigned Host",
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'size': 50,
                'style': 'width:50%',
                'class': 'form-control'}
            ),
            'description': TinyMCEWidget(
                mce_attrs={
                    'width': '90%',
                },
                attrs={
                    'style': 'padding-right: 100px',
                }
            ),
        }


class IpaddressForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(IpaddressForm, self).__init__(*args, **kwargs)
        logger.info("IpaddressForm - ")

    class Meta:
        fields = ("ip", "description", "hosts")
        model = Ipaddress
        labels = {
            "ip": "IP",
            "description": "Description",
            "hosts": "Assigned Host",
        }


class ProfileForm(forms.ModelForm):

    def __init__(self, inv_pk=0, *args, **kwargs):
        # user = kwargs.pop("user", None)
        super(ProfileForm, self).__init__(*args, **kwargs)
        logger.info("ProfileFormCall - ")
        self.fields['inv'].initial = inv_pk
        # self.fields['client'].queryset = Client.objects.filter(company=company)

    inv = forms.ModelChoiceField(
        label='Investigation:',
        queryset=Inv.objects.all(),
        required=False,
        empty_label="--Select--",
        widget=forms.Select(
            attrs={
                'class': 'selectpicker show-tick form-control',  # form-control
                'data-live-search': 'true',
                'data-width': 'auto',
                'data-style': 'btn-default btn-sm',
                'style': 'width:50%',
            }
        )
    )

    class Meta:
        fields = ("username", "userid", "email", "jobtitle", "host", "ip", "location",
                  "department", "location_contact", "inv", "description")
        model = Profile
        labels = {
            "description": "Description",
            "jobtitle": "Job Title",
            "location_contact": "Location Contact",
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'size': 50,
                'style': 'width:50%',
                'class': 'form-control'}
            ),
            'userid': forms.TextInput(attrs={
                'size': 30,
                'style': 'width:50%',
                'class': 'form-control'}
            ),
            'jobtitle': forms.TextInput(attrs={
                'size': 50,
                'style': 'width:50%',
                'class': 'form-control'}
            ),
            'email': forms.EmailInput(attrs={
                'size': 50,
                'style': 'width:50%',
                'class': 'form-control'}
            ),
            'ip': forms.TextInput(attrs={
                'size': 39,
                'maxlength': 39,
                'style': 'width:50%',
                'class': 'form-control'}
            ),
            'host': forms.TextInput(attrs={
                'size': 30,
                'style': 'width:50%',
                'class': 'form-control'}
            ),
            'location': forms.TextInput(attrs={
                'size': 30,
                'style': 'width:50%',
                'class': 'form-control'}
            ),
            'department': forms.TextInput(attrs={
                'size': 30,
                'style': 'width:50%',
                'class': 'form-control'}
            ),
            'location_contact': forms.TextInput(attrs={
                'size': 30,
                'style': 'width:50%',
                'class': 'form-control'}
            ),

            'description': TinyMCEWidget(
                mce_attrs={
                    'width': '90%',
                },
                attrs={
                    'style': 'padding-right: 100px',
                }
            ),
        }


##### CRUD TEST
# from django import forms
# from .models import Host
#
# class HostFormAjax(forms.ModelForm):
#     class Meta:
#         model = Host
#         fields = ['name','created_by']

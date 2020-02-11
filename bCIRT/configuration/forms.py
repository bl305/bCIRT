# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : configuration/forms.py
# Author            : Balazs Lendvay
# Date created      : 2019.07.27
# Purpose           : Forms file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.07.29  Lendvay     1      Initial file
# **********************************************************************;
from django import forms
from tinymce import TinyMCE
from .models import UpdatePackage, ConnectionItem, ConnectionItemField, SettingsCategory, SettingsUser, SettingsSystem
# Get the user so we can use this
from django.contrib.auth import get_user_model
import logging
logger = logging.getLogger('log_file_verbose')
User = get_user_model()


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class UpdatePackageForm(forms.ModelForm):
    # def __init__(self, conf_pk=0, *args, **kwargs):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(UpdatePackageForm, self).__init__(*args, **kwargs)
        logger.info("UpdatePackageForm - "+str(user))
        self.fields['user'].initial = user

        # self.fields['conf_pk'].initial = conf_pk

    user = forms.ModelChoiceField(
        label='Owner*',
        queryset=User.objects.all(),
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
        fields = ("updateversion", "user", "description", "fileRef")
        model = UpdatePackage
        labels = {
            "updateversion": "Version*",
            "description": "Description*",
            "fileRef": "Attachment",
        }
        widgets = {
            'description': TinyMCEWidget(
                mce_attrs={
                    'width': '95%',
                },
                attrs={
                    'style': 'padding-right: 100px',
                }
            ),
            'updateversion': forms.TextInput(attrs={
                'size': 18,
                'style': 'width:50%;',
                'class': 'form-control'}
            ),

        }


class ConnectionItemForm(forms.ModelForm):
    #  inv_pk and task_pk defaults to zero as they are not needed for updates
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(ConnectionItemForm, self).__init__(*args, **kwargs)
        logger.info("ConnectionItemForm - "+str(user))
        # self.fields['user'].initial = user

    #   fileRef = forms.FileField(widget=CustomClearableFileInput)
    class Meta:
        fields = ("name", "enabled", "description")
        model = ConnectionItem
        labels = {
            "description": "Description*",
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


class ConnectionItemFieldForm(forms.ModelForm):
    #  inv_pk and task_pk defaults to zero as they are not needed for updates
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(ConnectionItemFieldForm, self).__init__(*args, **kwargs)
        logger.info("ConnectionItemFieldForm - "+str(user))
        # self.fields['user'].initial = user

    connectionitemid = forms.ModelChoiceField(
        label='ConnectionItem*',
        queryset=ConnectionItem.objects.filter(enabled=True),
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

    #   fileRef = forms.FileField(widget=CustomClearableFileInput)
    class Meta:
        fields = ("connectionitemid", "connectionitemfieldname", "connectionitemfieldvalue", "encryptvalue")
        model = ConnectionItemField
        labels = {
            "connectionitemfieldname": "Name*",
            "connectionitemfieldvalue": "Value*",
            "encryptvalue": "Encrypt Value*",
        }
        widgets = {
            'connectionitemfieldname': forms.TextInput(attrs={
                'size': 50,
                'style': 'width:50%',
                'class': 'form-control'}
            ),
            'connectionitemfieldvalue': forms.TextInput(attrs={
                'size': 256,
                'style': 'width:50%;',
                'class': 'form-control'}
            ),
        }


class SettingsUserForm(forms.ModelForm):
    #  inv_pk and task_pk defaults to zero as they are not needed for updates
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(SettingsUserForm, self).__init__(*args, **kwargs)
        logger.info("SettingsUserForm - "+str(user))
        # self.fields['user'].initial = user

    settingcategory = forms.ModelChoiceField(
        label='Category',
        queryset=SettingsCategory.objects.filter(enabled=True),
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

    #   fileRef = forms.FileField(widget=CustomClearableFileInput)
    class Meta:
        fields = ("settingname", "settingvalue", "settingcategory", "enabled")
        model = SettingsUser
        labels = {
            "settingname": "Name*",
            "settingvalue": "Value",
            "enabled": "Enabled*",
        }
        widgets = {
            'settingname': forms.TextInput(attrs={
                'size': 25,
                'style': 'width:50%',
                'class': 'form-control'}
            ),
            'settingvalue': forms.TextInput(attrs={
                'size': 255,
                'style': 'width:50%;',
                'class': 'form-control'}
            ),
        }


class SettingsSystemForm(forms.ModelForm):
    #  inv_pk and task_pk defaults to zero as they are not needed for updates
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(SettingsSystemForm, self).__init__(*args, **kwargs)
        logger.info("SettingsSystemForm - "+str(user))
        # self.fields['user'].initial = user

    settingcategory = forms.ModelChoiceField(
        label='Category',
        queryset=SettingsCategory.objects.filter(enabled=True),
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

    #   fileRef = forms.FileField(widget=CustomClearableFileInput)
    class Meta:
        fields = ("settingname", "settingvalue", "settingcategory", "enabled")
        model = SettingsSystem
        labels = {
            "settingname": "Name*",
            "settingvalue": "Value",
            "enabled": "Enabled*",
        }
        widgets = {
            'settingname': forms.TextInput(attrs={
                'size': 25,
                'style': 'width:50%',
                'class': 'form-control'}
            ),
            'settingvalue': forms.TextInput(attrs={
                'size': 255,
                'style': 'width:50%;',
                'class': 'form-control'}
            ),
        }

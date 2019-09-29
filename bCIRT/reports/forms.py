# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : reports/forms.py
# Author            : Balazs Lendvay
# Date created      : 2019.07.27
# Purpose           : Forms file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.07.29  Lendvay     1      Initial file
# **********************************************************************;
from django import forms
# Get the user so we can use this
from django.contrib.auth import get_user_model
import logging

from django.forms.widgets import SplitDateTimeWidget  # , ClearableFileInput

logger = logging.getLogger('log_file_verbose')
User = get_user_model()

class CustomReportForm(forms.Form):
    # enddate = forms.DateField(
    #     input_formats=['%d/%m/%Y %H:%M'],
    #     label='End',
    #     widget=forms.SelectDateWidget
    # )
    # holiday = forms.DateField(widget=forms.TextInput(attrs=
    # {
    #     'class': 'datepicker'
    # }))

    starttime = forms.SplitDateTimeField(
        required=False,
        label='StartTime',
        input_date_formats=['%m/%d/%Y'],
        input_time_formats=['%H:%M'],
        widget=SplitDateTimeWidget(
            date_format='%m/%d/%Y',
            time_format='%H:%M',
            attrs={
                'class': 'form-control',
                'style': 'width:100px',
            }
        )
    )
    endtime = forms.SplitDateTimeField(
        required=False,
        label='Endtime',
        input_date_formats=['%m/%d/%Y'],
        input_time_formats=['%H:%M'],
        widget=SplitDateTimeWidget(
            date_format='%m/%d/%Y',
            time_format='%H:%M',
            attrs={
                'class': 'form-control',
                'style': 'width:100px',
            }
        )
    )
    #     name = forms.CharField()
    #     message = forms.CharField(widget=forms.Textarea)
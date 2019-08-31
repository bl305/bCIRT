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
logger = logging.getLogger('log_file_verbose')
User = get_user_model()

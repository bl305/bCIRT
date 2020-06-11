# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : invs/templatetags/field_type.py
# Author            : Balazs Lendvay
# Date created      : 2020.01.22
# Purpose           : istaskreadonly file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2020.01.22  Lendvay     1      Initial file
# **********************************************************************;
# Display field types in templates
from django import template
from django.template.defaultfilters import stringfilter
from tasks.models import taskreadonly, taskcompleted, evidencereadonly

register = template.Library()

@register.filter(name='istaskreadonly')
@stringfilter
def istaskreadonly(value):
    return taskreadonly(value)

@register.filter(name='istaskcompleted')
@stringfilter
def istaskcompleted(value):
    return taskcompleted(value)

@register.filter(name='isevidencereadonly')
def isevidencereadonly(value):
    return evidencereadonly(int(value))

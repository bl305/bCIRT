# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : invs/templatetags/getevidencedata.py
# Author            : Balazs Lendvay
# Date created      : 2020.01.29
# Purpose           : istaskreadonly file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2020.01.29  Lendvay     1      Initial file
# **********************************************************************;
# Display field types in templates
from django import template
from django.template.defaultfilters import stringfilter
from tasks.models import get_actionq_list_by_evidence,\
    get_attribute_list_by_evidence,\
    get_attribute_list_by_evidence_values,\
    get_evidencesameitems_inv_values

register = template.Library()

@register.filter(name='getactionqlistbyevidence')
@stringfilter
def getactionqlistbyevidence(value):
    return get_actionq_list_by_evidence(value)

@register.filter(name='getattributelistbyevidence')
@stringfilter
def getattributelistbyevidence(value):
    return get_attribute_list_by_evidence(value)

@register.filter(name='getattributelistvaluesbyevidence')
@stringfilter
def getattributelistvaluesbyevidence(value):
    return get_attribute_list_by_evidence_values(value)

@register.filter(name='getsameattributelistbyevidence')
@stringfilter
def getsameattributelistbyevidence(value):
    return get_evidencesameitems_inv_values(value)


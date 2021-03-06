# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : knowledgebase/resources.py
# Author            : Balazs Lendvay
# Date created      : 2020.03.31
# Purpose           : Resources file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2020.03.31  Lendvay     1      Initial file
# **********************************************************************;
from import_export import resources
from .models import KnowledgeBase, KnowledgeBaseFormat


class KnowledgeBaseResource(resources.ModelResource):
    class Meta:
        model = KnowledgeBase


class KnowledgeBaseFormatResource(resources.ModelResource):
    class Meta:
        model = KnowledgeBaseFormat

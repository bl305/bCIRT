# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : tasks/resources.py
# Author            : Balazs Lendvay
# Date created      : 2019.07.27
# Purpose           : Resources file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.07.29  Lendvay     1      Initial file
# **********************************************************************;
from import_export import resources
from .models import Task, TaskCategory, TaskPriority, TaskStatus, TaskType,\
    TaskTemplate, TaskVar, TaskVarCategory, TaskVarType, \
    Playbook, PlaybookTemplate, PlaybookTemplateItem,\
    Evidence, EvidenceFormat, EvidenceAttr, EvidenceAttrFormat, EvReputation, \
    Action, Automation, ActionGroup, ActionGroupMember, \
    ScriptType, ScriptOs, ScriptCategory, ScriptOutput, OutputTarget, ScriptInput,\
    Type, ActionQ, ActionQStatus, MitreAttck_Tactics, MitreAttck_Techniques

class EvidenceResource(resources.ModelResource):
    class Meta:
        model = Evidence


class EvidenceFormatResource(resources.ModelResource):
    def xxxbefore_import(self, dataset, using_transactions, dry_run, **kwargs):
        pass
        # print(dataset)

    def xxxbefore_export(self, queryset, *args, **kwargs):
        fieldnames = queryset.get_export_headers()
        myfields = queryset.get_fields()
        myvalues = queryset.get_export_fields()
        for ii in myfields:
            print(ii)
        print("x")
        print(queryset.get_field_name(myvalues[0]))
        print("X")

        print(queryset.get_queryset())
        print(queryset)

    # def export(queryset=None, *args, **kwargs):
        # print(queryset.get_queryset())
        # print(queryset.get_export_fields()[0])
        # print(queryset.get_user_visible_fields())
        # pass
    class Meta:
        model = EvidenceFormat


class EvidenceAttrResource(resources.ModelResource):
    class Meta:
        model = EvidenceAttr


class EvReputationResource(resources.ModelResource):
    class Meta:
        model = EvReputation


class EvidenceAttrFormatResource(resources.ModelResource):
    class Meta:
        model = EvidenceAttrFormat


class ActionResource(resources.ModelResource):
    class Meta:
        model = Action


class ActionGroupResource(resources.ModelResource):
    class Meta:
        model = ActionGroup


class ActionGroupMemberResource(resources.ModelResource):
    class Meta:
        model = ActionGroupMember


class AutomationResource(resources.ModelResource):
    class Meta:
        model = Automation


class ActionGroupResource(resources.ModelResource):
    class Meta:
        model = ActionGroup


class ActionGroupMemberResource(resources.ModelResource):
    class Meta:
        model = ActionGroupMember


class ScriptTypeResource(resources.ModelResource):
    class Meta:
        model = ScriptType


class ScriptOsResource(resources.ModelResource):
    class Meta:
        model = ScriptOs


class ScriptCategoryResource(resources.ModelResource):
    class Meta:
        model = ScriptCategory


class ScriptOutputResource(resources.ModelResource):
    class Meta:
        model = ScriptOutput


class ScriptInputResource(resources.ModelResource):
    class Meta:
        model = ScriptInput


class OutputTargetResource(resources.ModelResource):
    class Meta:
        model = OutputTarget


class TypeResource(resources.ModelResource):
    class Meta:
        model = Type


class ActionQResource(resources.ModelResource):
    class Meta:
        model = ActionQ


class ActionQStatusResource(resources.ModelResource):
    class Meta:
        model = ActionQStatus


class TaskResource(resources.ModelResource):
    class Meta:
        model = Task


class TaskCategoryResource(resources.ModelResource):
    class Meta:
        model = TaskCategory


class TaskPriorityResource(resources.ModelResource):
    class Meta:
        model = TaskPriority


class TaskStatusResource(resources.ModelResource):
    class Meta:
        model = TaskStatus


class TaskTypeResource(resources.ModelResource):
    class Meta:
        model = TaskType


class TaskTemplateResource(resources.ModelResource):
    class Meta:
        model = TaskTemplate


class TaskVarResource(resources.ModelResource):
    class Meta:
        model = TaskVar


class TaskVarCategoryResource(resources.ModelResource):
    class Meta:
        model = TaskVarCategory


class TaskVarTypeResource(resources.ModelResource):
    class Meta:
        model = TaskVarType


class PlaybookResource(resources.ModelResource):
    class Meta:
        model = Playbook


class PlaybookTemplateResource(resources.ModelResource):
    class Meta:
        model = PlaybookTemplate


class PlaybookTemplateItemResource(resources.ModelResource):
    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        pbtmp = PlaybookTemplate.objects.first()
        pbtmpi=PlaybookTemplateItem.objects.get_or_create(pk=pbtmp)
        print(pbtmpi)
        pass

    class Meta:
        model = PlaybookTemplateItem


class MitreAttck_TacticsResource(resources.ModelResource):
    class Meta:
        model = MitreAttck_Tactics


class MitreAttck_TechniquesResource(resources.ModelResource):
    class Meta:
        model = MitreAttck_Techniques

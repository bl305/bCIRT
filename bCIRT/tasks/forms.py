# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : tasks/forms.py
# Author            : Balazs Lendvay
# Date created      : 2019.07.27
# Purpose           : Forms file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.07.29  Lendvay     1      Initial file
# 2019.08.19  Lendvay     1      Added "enabled" ot the form for actions
# **********************************************************************;
from django import forms
from tinymce import TinyMCE
from .models import Task, TaskCategory, TaskPriority, TaskStatus, TaskTemplate, TaskType, TaskVar, TaskVarCategory, \
    TaskVarType, Type, EvidenceFormat, EvidenceAttrFormat, EvidenceAttr, Evidence, EvReputation, \
    Action, ActionGroup, ActionGroupMember, Playbook, PlaybookTemplate, PlaybookTemplateItem, \
    ScriptType, ScriptOutput, ScriptCategory, ScriptInput, OutputTarget,\
    Inv, MitreAttck_Tactics, Automation
from assets.models import Host, Hostname, Ipaddress, Profile
from configuration.models import ConnectionItem
# from django.core.exceptions import ValidationError
from django.forms.widgets import SplitDateTimeWidget  # , ClearableFileInput
# Get the user so we can use this
from django.contrib.auth import get_user_model
import logging
User = get_user_model()
logger = logging.getLogger('log_file_verbose')


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


# class CustomClearableFileInput(ClearableFileInput):
#     template_name = 'invs/customclearablefileinput.html'
class ActionForm(forms.ModelForm):
    #  inv_pk and task_pk defaults to zero as they are not needed for updates
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(ActionForm, self).__init__(*args, **kwargs)
        logger.info("ActionForm - "+str(user))
        self.fields['user'].initial = user

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

    timeout = forms.IntegerField(
        label='Timeout (sec)',
        min_value=0,
    )

    automationid = forms.ModelChoiceField(
        label="Automation",
        queryset=Automation.objects.filter(enabled=True),
        empty_label="--None--",
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

    scriptoutput = forms.ModelChoiceField(
        label="Output Format*",
        queryset=ScriptOutput.objects.filter(enabled=True),
        empty_label="--None--",
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

    scriptinput = forms.ModelChoiceField(
        label="Input Source*",
        queryset=ScriptInput.objects.filter(enabled=True),
        empty_label="--None--",
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

    scriptinputattrtype = forms.ModelChoiceField(
        label="Input Attribute Filter",
        queryset=EvidenceAttrFormat.objects.filter(enabled=True),
        empty_label="--None--",
        required=False,
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

    outputtarget = forms.ModelChoiceField(
        label="Output Target*",
        queryset=OutputTarget.objects.filter(enabled=True),
        empty_label="--None--",
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

    outputdescformat = forms.ModelChoiceField(
        label="Output Evidence Format*",
        queryset=EvidenceFormat.objects.filter(enabled=True),
        empty_label="--None--",
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

    scriptoutputtype = forms.ModelChoiceField(
        label="Output Data Type*",
        queryset=EvidenceAttrFormat.objects.filter(enabled=True),
        empty_label="--None--",
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

    connectionitemid = forms.ModelChoiceField(
        label="Use Connection",
        queryset=ConnectionItem.objects.filter(enabled=True),
        empty_label="--None--",
        required=False,
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
        fields = ("user", "title", "version", "enabled", "automationid", "scriptinput", "scriptinputattrtype",
                  "scriptinputattrtypeall", "scriptoutput",  "scriptoutputtype", "outputtarget", "outputdescformat",
                  "argument", "connectionitemid", "timeout", "fileRef", "description")
        model = Action
        labels = {
            "description": "Description*",
            "fileRef": "Attachment",
            'argument': 'Argument (override: $FILE$ can be used to refer to the evidence file, $EVIDENCE$ for '
                        'the description/attribute, $OUTDIR$ for any output files)',
            "timeout": "Timeout (sec)",
            'title': 'Title*',
            'version': 'Version*',
            'scriptoutput': 'Script output format',
            'outputtarget': 'Output Target*',
            'scriptinputattrtypeall': 'Run on all filtered attributes',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'size': 50,
                'style': 'width:50%',
                'class': 'form-control'}
            ),
            'version': forms.TextInput(attrs={
                'size': 20,
                'style': 'width:50%',
                'class': 'form-control'}
            ),
            'argument': forms.Textarea(attrs={
                'rows': '1',
                'cols': '25',
                'style': 'width:50%',
                'class': 'form-control'}
            ),
            'timeout': forms.NumberInput(attrs={
                'style': 'width:20%',
                'class': 'form-control'}
            ),
            # 'fileRef': CustomClearableFileInput,
            'description': TinyMCEWidget(
                mce_attrs={
                    'width': '90%',

                    # 'readonly': True,
                    # 'menubar': False,
                    # 'toolbar': False,
                    #                    'autoresize_overflow_padding': 10,

                },
                attrs={
                    'style': 'padding-right: 100px',
                }
            ),
        }


class ActionGroupForm(forms.ModelForm):
    #  inv_pk and task_pk defaults to zero as they are not needed for updates
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(ActionGroupForm, self).__init__(*args, **kwargs)
        logger.info("ActionGroupForm - "+str(user))
        # self.fields['user'].initial = user

    #   fileRef = forms.FileField(widget=CustomClearableFileInput)
    class Meta:
        fields = ("name", "enabled", "description")
        model = ActionGroup
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


class ActionGroupMemberForm(forms.ModelForm):
    #  inv_pk and task_pk defaults to zero as they are not needed for updates
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(ActionGroupMemberForm, self).__init__(*args, **kwargs)
        logger.info("ActionGroupMemberForm - "+str(user))
        # self.fields['user'].initial = user

    actionid = forms.ModelChoiceField(
        label='Action*',
        queryset=Action.objects.filter(enabled=True),
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

    actiongroupid = forms.ModelChoiceField(
        label='Action Group*',
        queryset=ActionGroup.objects.filter(enabled=True),
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
        fields = ("actiongroupid", "actionid")
        model = ActionGroupMember
        # labels = {
        #     "description": "Description*",
        # }
        widgets = {
        }


class TaskForm(forms.ModelForm):

    def __init__(self, inv_pk=0, *args, **kwargs):
        user = kwargs.pop("user", None)

        super(TaskForm, self).__init__(*args, **kwargs)
        logger.info("TaskForm - "+str(user))
        self.fields['inv'].initial = inv_pk
        if kwargs.get('instance'):
            current_pk = kwargs.get('instance').pk
            self.fields['parent'].queryset = Task.objects.all().exclude(pk=current_pk)
            self.fields['inputfrom'].queryset = Task.objects.all().exclude(pk=current_pk)
            # The actiontarget can be the task itself also, so no need to exclude
            # self.fields['actiontarget'].queryset = Task.objects.all().exclude(pk=current_pk)
        # else:
        #     current_pk = 0
        self.fields['user'].initial = user
        self.fields['status'].initial = 3
        self.fields['priority'].initial = 1

    status = forms.ModelChoiceField(
        label='Status*',
        queryset=TaskStatus.objects.filter(enabled=True),
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

    user = forms.ModelChoiceField(
        label='Assigned to',
        queryset=User.objects.all(),
        empty_label="--Select--",
        required=False,
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

    action = forms.ModelChoiceField(
        label='Action',
        #  queryset overwritten in init
        queryset=Action.objects.filter(enabled=True),
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

    actiontarget = forms.ModelChoiceField(
        label='Action Target Task',
        #  queryset overwritten in init
        queryset=Task.objects.all(),
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

    parent = forms.ModelChoiceField(
        label='Parent',
        #  queryset overwritten in init
        queryset=Task.objects.all(),
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

    inputfrom = forms.ModelChoiceField(
        label='Input Task',
        #  queryset overwritten in init
        queryset=Task.objects.all(),
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

    inv = forms.ModelChoiceField(
        label='Investigation',
        queryset=Inv.objects.exclude(status='2'),
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

    category = forms.ModelChoiceField(
        label='Category*',
        queryset=TaskCategory.objects.filter(enabled=True),
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

    priority = forms.ModelChoiceField(
        label='Priority*',
        queryset=TaskPriority.objects.filter(enabled=True),
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

    type = forms.ModelChoiceField(
        label='Type*',
        queryset=TaskType.objects.filter(enabled=True),
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

    starttime = forms.SplitDateTimeField(
        required=False,
        label='Start of task',
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
        label='End of task',
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

    class Meta:
        model = Task
        fields = ('title',
                  'status',
                  'user',
                  'parent',
                  'inputfrom',
                  'inv',
                  # 'playbook',
                  'category',
                  'priority',
                  'type',
                  'action',
                  'actiontarget',
                  'summary',
                  'description',
                  'starttime',
                  'endtime')
        labels = {
            'title': 'Title*',
            'user': "Assigned to",
            'summary': "Summary",
            'description': 'Description*',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'size': 50,
                'style': 'width:50%',
                'class': 'form-control'}
            ),
            'summary': forms.Textarea(attrs={
                'rows': '5',
                'cols': '68',
                'style': 'width:90%',
                'class': 'form-control'}
            ),
            'description': TinyMCEWidget(
                mce_attrs={
                    'width': '95%',
                },
                attrs={
                    'style': 'padding-right: 100px',
                }
            ),
        }


class TaskTemplateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)

        super(TaskTemplateForm, self).__init__(*args, **kwargs)
        logger.info("TaskTemplateForm - "+str(user))
        # current_pk = kwargs.get('instance').pk
        if kwargs.get('instance'):
            current_pk = kwargs.get('instance').pk
            self.fields['actiontarget'].queryset = TaskTemplate.objects.all().exclude(pk=current_pk)
        # define some defaults
        self.fields['status'].initial = 1
        self.fields['user'].initial = None
        self.fields['priority'].initial = 1
        self.fields['category'].initial = 1

    status = forms.ModelChoiceField(
        label='Status*',
        queryset=TaskStatus.objects.filter(enabled=True).order_by('name'),
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

    user = forms.ModelChoiceField(
        label='Assigned to',
        queryset=User.objects.all(),
        empty_label="--Select--",
        required=False,
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

    action = forms.ModelChoiceField(
        label='Action',
        #  queryset overwritten in init
        queryset=Action.objects.all(),
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

    actiontarget = forms.ModelChoiceField(
        label='Action Target Task',
        #  queryset overwritten in init
        queryset=TaskTemplate.objects.all(),
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

    category = forms.ModelChoiceField(
        label='Category*',
        queryset=TaskCategory.objects.filter(enabled=True),
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

    priority = forms.ModelChoiceField(
        label='Priority*',
        queryset=TaskPriority.objects.filter(enabled=True),
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

    type = forms.ModelChoiceField(
        label='Type*',
        queryset=TaskType.objects.filter(enabled=True),
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
        model = TaskTemplate
        fields = ('tasktemplatename',
                  'enabled',
                  'title',
                  'status',
                  'user',
                  'category',
                  'priority',
                  'type',
                  'action',
                  'actiontarget',
                  'summary',
                  'description',
                  )
        labels = {
            'tasktemplatename': "Template Name*",
            'user': "Assigned to",
            'summary': "Summary",
            'description': 'Description*',
            'title': 'Title*',
        }
        widgets = {
            'tasktemplatename': forms.TextInput(attrs={
                'size': 50,
                'style': 'width:50%',
                'class': 'form-control'}
            ),
            'title': forms.TextInput(attrs={
                'size': 50,
                'style': 'width:50%',
                'class': 'form-control'}
            ),
            'summary': forms.Textarea(attrs={
                'rows': '5',
                'cols': '68',
                'style': 'width:90%',
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


class TaskVarForm(forms.ModelForm):

    def __init__(self, task_pk=0, tasktmp_pk=0, *args, **kwargs):
        user = kwargs.pop("user", None)

        super(TaskVarForm, self).__init__(*args, **kwargs)
        logger.info("TaskVarForm - "+str(user))
        self.fields['task'].initial = task_pk
        self.fields['tasktemplate'].initial = tasktmp_pk
        self.fields['user'].initial = user

    user = forms.ModelChoiceField(
        label='Owner:',
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

    task = forms.ModelChoiceField(
        label='Task',
        queryset=Task.objects.exclude(status='2'),
        empty_label="--Select--",
        required=False,
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

    tasktemplate = forms.ModelChoiceField(
        label='Task Template',
        queryset=TaskTemplate.objects.filter(enabled=True),
        empty_label="--Select--",
        required=False,
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

    category = forms.ModelChoiceField(
        label='Category*',
        queryset=TaskVarCategory.objects.filter(enabled=True),
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

    type = forms.ModelChoiceField(
        label='Type*',
        queryset=TaskVarType.objects.filter(enabled=True),
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
        model = TaskVar
        fields = ('category',
                  'type',
                  'task',
                  'tasktemplate',
                  'name',
                  'value',
                  'required',
                  'enabled',
                  'description',
                  )
        labels = {
            'description': 'Description*',
            'name': 'Name*',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'size': 50,
                'style': 'width:50%',
                'class': 'form-control'}
            ),
            'value': forms.Textarea(attrs={
                'rows': '5',
                'cols': '68',
                'style': 'width:90%',
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


class PlaybookForm(forms.ModelForm):
    # inv_pk and task_pk defaults to zero as they are not needed for updates
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(PlaybookForm, self).__init__(*args, **kwargs)
        logger.info("PlaybookForm - "+str(user))
        self.fields['user'].initial = user

    user = forms.ModelChoiceField(
        label='Owner:',
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

    inv = forms.ModelChoiceField(
        label='Investigation',
        queryset=Inv.objects.all(),
        empty_label="--Select--",
        required=False,
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

    # fileRef = forms.FileField(widget=CustomClearableFileInput)
    class Meta:
        fields = ("user", "name", "version", "inv", "description")
        model = Playbook
        labels = {
            'user': 'Owner',
            'name': 'Name*',
            'description': 'Description*',
        }
        widgets = {
            'description': TinyMCEWidget(
                mce_attrs={
                    'width': '90%',
                },
                attrs={
                    'style': 'padding-right: 100px',
                }
            ),
        }


class PlaybookTemplateForm(forms.ModelForm):
    # inv_pk and task_pk defaults to zero as they are not needed for updates
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(PlaybookTemplateForm, self).__init__(*args, **kwargs)
        logger.info("PlaybookTemplateForm - "+str(user))
        self.fields['user'].initial = user

    user = forms.ModelChoiceField(
        label='Owner:',
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

    # fileRef = forms.FileField(widget=CustomClearableFileInput)
    class Meta:
        fields = ("name", "user", "enabled", "version", "description")
        model = PlaybookTemplate
        labels = {
            "user": "Owner",
            "description": "Description*",
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'size': 50,
                'style': 'width:30%;',
                'class': 'form-control'}
            ),
            'version': forms.TextInput(attrs={
                'size': 20,
                'style': 'width:10%;',
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


class PlaybookTemplateItemForm(forms.ModelForm):

    play_pk = None

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        self.play_pk = kwargs.pop('play_pk', None)
        super(PlaybookTemplateItemForm, self).__init__(*args, **kwargs)
        logger.info("PlaybookTemplateItemForm - "+str(user))
        self.fields['playbooktemplateid'].initial = self.play_pk
        self.fields['user'].initial = user
        # self.fields['itemorder'].initial = 100
        from django.db.models import Max
        if PlaybookTemplateItem.objects.filter(playbooktemplateid=self.play_pk):
            self.fields['itemorder'].initial = int(PlaybookTemplateItem.objects.filter(playbooktemplateid=self.play_pk).aggregate(Max('itemorder'))['itemorder__max'])+1
        else:
            self.fields['itemorder'].initial = 100

        if kwargs.get('instance'):
            currentitem_pk = kwargs.get('instance').pk
        else:
            currentitem_pk = 0

        if self.play_pk != "0":

            # print("play_pk:"+str(self.play_pk))
            # self.fields['nexttask'].queryset = TaskTemplate.objects.filter(enabled=True).values('category','title')
            # self.fields['nexttask'].queryset = PlaybookTemplateItem.objects.filter(playbooktemplateid=self.play_pk)
            # xxx=TaskTemplate.objects.get(pk=PlaybookTemplateItem.objects.get(pk=self.play_pk).acttask.pk).pk
            try:
                if PlaybookTemplateItem.objects.get(pk=self.play_pk):
                    # actual_playbookitem = PlaybookTemplateItem.objects.get(pk=self.play_pk)
                    # actual_playbooktemplate = actual_playbookitem.playbooktemplateid.pk
                    # print("PBTITEM:"+str(actual_playbookitem))
                    #     print("PB:"+str(actual_playbooktemplate))
                    actual_playbooktemplate = PlaybookTemplateItem.objects.get(pk=currentitem_pk).playbooktemplateid.pk

                    # print("PBNEW:"+str(actual_playbooktemplate))
                    # print(PlaybookTemplateItem.objects.filter(playbooktemplateid=actual_playbooktemplate).
                    # exclude(pk=actual_playbookitem.pk))
                    # print("playbook:"+str(PlaybookTemplate.objects.get(pk=8)))
                    # self.fields['nexttask'].queryset = PlaybookTemplateItem.objects.filter(
                    # playbooktemplateid=self.play_pk)
                    #     self.fields['nexttask'].queryset = PlaybookTemplateItem.objects.filter(
                    #     playbooktemplateid=actual_playbooktemplate).exclude(pk=actual_playbookitem.pk)
                    self.fields['nexttask'].queryset = PlaybookTemplateItem.objects.filter(
                        playbooktemplateid=actual_playbooktemplate).exclude(pk=currentitem_pk)
                    self.fields['prevtask'].queryset = PlaybookTemplateItem.objects.filter(
                        playbooktemplateid=actual_playbooktemplate).exclude(pk=currentitem_pk)
                else:
                    self.fields['prevtask'].queryset = PlaybookTemplateItem.objects.filter(pk=0)
                    self.fields['nexttask'].queryset = PlaybookTemplateItem.objects.filter(pk=0)
            except Exception:
                # self.fields['nexttask'].queryset = PlaybookTemplateItem.objects.filter(pk=0)
                # self.fields['prevtask'].queryset = PlaybookTemplateItem.objects.filter(pk=0)
                self.fields['nexttask'].queryset = PlaybookTemplateItem.objects.filter(enabled=True)
                self.fields['prevtask'].queryset = PlaybookTemplateItem.objects.filter(enabled=True)
        else:
            # self.fields['nexttask'].queryset = TaskTemplate.objects.filter(enabled=True)
            self.fields['nexttask'].queryset = PlaybookTemplateItem.objects.filter(enabled=True)

    user = forms.ModelChoiceField(
        label='Owner:',
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

    playbooktemplateid = forms.ModelChoiceField(
        label='PlaybookTemplate*',
        queryset=PlaybookTemplate.objects.filter(enabled=True),
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

    prevtask = forms.ModelChoiceField(
            label="Previous Task",
            queryset=TaskTemplate.objects.filter(enabled=True),
            # the line above is overriden by the __INIT__ only allow available tasks
            empty_label="--None--",
            required=False,
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

    acttask = forms.ModelChoiceField(
        label="Actual Task*",
        queryset=TaskTemplate.objects.filter(enabled=True),
        empty_label="--None--",
        required=False,
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

    nexttask = forms.ModelChoiceField(
            label="Next Task",
            queryset=TaskTemplate.objects.filter(enabled=True),
            # the line above is overriden by the __INIT__ only allow available tasks
            empty_label="--None--",
            required=False,
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
        model = PlaybookTemplateItem
        fields = ('user',
                  'enabled',
                  'playbooktemplateid',
                  'prevtask',
                  'acttask',
                  'itemorder',
                  'nexttask',
                  'description',
                  )
        labels = {
            'user': 'Owner',
            'description': 'Description*',
        }
        widgets = {
            'itemorder': forms.TextInput(attrs={
                'size': 2,
                'style': 'width:70px;',
                'maxlength': 5,
                'class': 'form-control'}
            ),
            # 'itemorder': forms.IntegerField(
            # max_value=32767,
            # min_value=-32768
            # ),
            'description': TinyMCEWidget(
                mce_attrs={
                    'width': '90%',
                },
                attrs={
                    'style': 'padding-right: 100px',
                }
            ),
        }


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
    # myfield=forms.ModelMultipleChoiceField(queryset=Terminal.objects.all() )
    # the nadd this to the "fields"

    def __init__(self, inv_pk=0, *args, **kwargs):
        # user = kwargs.pop("user", None)
        super(ProfileForm, self).__init__(*args, **kwargs)
        logger.info("ProfileFormCall - ")
        self.fields['inv'].initial = inv_pk
        # self.fields['client'].queryset = Client.objects.filter(company=company)

    # def clean(self):
    #     cleaned_data = super(ProfileForm, self).clean()  # Get the cleaned data from default clean,
    #     returns cleaned_data
    #     field1 = cleaned_data.get("username")
    #     field2 = cleaned_data.get("userid"),
    #     field3 = cleaned_data.get("email")
    #     field4 = cleaned_data.get("host"),
    #     field5 = cleaned_data.get("ip")

        # if (field1 is None) and \
        #         (field2 == (None,)) and \
        #         (field3 is None) and \
        #         (field4 == (None,)) and \
        #         (field5 == ""):
        #
        #     raise ValidationError(_('You must fill in one of the fields.'))
        # return cleaned_data

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
        fields = ("username", "userid", "email", "host", "ip", "location", "department", "location_contact", "inv",
                  "description")
        model = Profile
        labels = {
            "description": "Description",
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


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


# class CustomClearableFileInput(ClearableFileInput):
#     template_name = 'invs/customclearablefileinput.html'
class EvidenceForm(forms.ModelForm):
    # inv_pk and task_pk defaults to zero as they are not needed for updates
    # evidenceformat=2
    def __init__(self, inv_pk=0, task_pk=0, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(EvidenceForm, self).__init__(*args, **kwargs)
        logger.info("EvidenceForm - "+str(user))
        self.fields['user'].initial = user

        self.fields['inv'].initial = inv_pk
        self.fields['task'].initial = task_pk
        if EvidenceFormat.objects.get(pk=2):
            self.fields['evidenceformat'].initial = EvidenceFormat.objects.get(pk=2)
        # if kwargs.get('instance'):
        #     current_pk = kwargs.get('instance').pk
        #     self.evidenceformat=Evidence.objects.get(pk=current_pk).evidenceformat

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

    inv = forms.ModelChoiceField(
        label="Related Investigation",
        # queryset=Inv.objects.exclude(status='2'),  # CLOSED
        queryset=Inv.objects.exclude(status=2),
        empty_label="--None--",
        required=False,
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

    task = forms.ModelChoiceField(
        label="Related Task",
        # queryset=Task.objects.exclude(status='2'),  #  exclude closed task
        queryset=Task.objects.exclude(status=2),
        empty_label="--None--",
        required=False,
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

    parent = forms.ModelChoiceField(
        label='Parent',
        queryset=Evidence.objects.all(),
        empty_label="--Select--",
        required=False,
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

    evidenceformat = forms.ModelChoiceField(
        label="Evidence format*",
        queryset=EvidenceFormat.objects.filter(enabled=True),  # .values_list('name',flat=True),
        empty_label="--None--",
        required=True,
        # initial=EvidenceFormat.objects.get(pk=2),
        widget=forms.Select(
            attrs={
                'class': 'selectpicker show-tick form-control',  # form-control
                'data-live-search': 'true',
                'data-width': 'auto',
                'data-style': 'btn-default btn-sm',
                'style': 'width:50%',
                'onChange': '''
                if ($(this).val() == 1) { editorRAW();};
                if ($(this).val() == 2) { editorTINYMCE();};      
                '''
            }
        )
    )

    mitretactic = forms.ModelChoiceField(
        label="MITRE ATTCK Tactics*",
        # queryset=Task.objects.exclude(status='2'),  #  exclude closed task
        queryset=MitreAttck_Tactics.objects.exclude(enabled=False),
        empty_label="--None--",
        required=True,
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
    # fileRef = forms.FileField(widget=CustomClearableFileInput)

    class Meta:
        fields = ("user", "inv", "task", "parent", "evidenceformat", "mitretactic", "description", "fileRef")
        # fields = ( "user", "inv", "description")
        model = Evidence
        labels = {
            "description": "Description*",
            "fileRef": "Attachment",
            "parent": "Parent",
        }
        widgets = {
            # 'fileRef': CustomClearableFileInput,
            'description': TinyMCEWidget(
                mce_attrs={
                    'width': '95%',
                },
                attrs={
                    'style': 'padding-right: 100px',
                }
            ),
        }


class EvidenceAttrForm(forms.ModelForm):
    # inv_pk and task_pk defaults to zero as they are not needed for updates
    # evidenceformat=2
    def __init__(self, pk=0, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(EvidenceAttrForm, self).__init__(*args, **kwargs)
        logger.info("EvidenceAttrForm - "+str(user))
        self.fields['user'].initial = user
        self.fields['ev'].initial = pk

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

    ev = forms.ModelChoiceField(
        label="Evidence*",
        queryset=Evidence.objects.all(),  # .values_list('name',flat=True),
        empty_label="--None--",
        required=True,
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

    evattrformat = forms.ModelChoiceField(
        label="Attribute format*",
        queryset=EvidenceAttrFormat.objects.filter(enabled=True).order_by('name'),  # .values_list('name',flat=True),
        empty_label="--None--",
        required=True,
        # initial=EvidenceAttrFormat.objects.get(pk=2),
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

    attr_reputation = forms.ModelChoiceField(
        label="Reputation",
        queryset=EvReputation.objects.filter(enabled=True),  # .values_list('name',flat=True),
        empty_label="--None--",
        # initial=EvidenceAttrFormat.objects.get(pk=2),
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
        fields = ("user", "ev", "evattrformat", "evattrvalue", "attr_reputation", "observable")
        model = EvidenceAttr
        labels = {
            "evattrvalue": "Value*",
            "observable": "Observable"
        }
        widgets = {
            'observable': forms.CheckboxInput(
                attrs={
                    'class': 'custom-control-input custom-control-label',
                }
            ),
            'evattrvalue': forms.TextInput(attrs={
                'size': 100,
                'style': 'width:50%',
                'class': 'form-control'}
            ),
        }

#########################################
    #
    # 'code': forms.Textarea(attrs={
    #     'rows': '10',
    #     'cols': '68',
    #     'style': 'width:90%',
    #     'class': 'form-control'}
    # ),


class AutomationForm(forms.ModelForm):
    #  inv_pk and task_pk defaults to zero as they are not needed for updates
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(AutomationForm, self).__init__(*args, **kwargs)
        logger.info("AutomationForm - "+str(user))
        self.fields['user'].initial = user

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

    type = forms.ModelChoiceField(
        label="Type*",
        queryset=Type.objects.filter(enabled=True),
        empty_label="--None--",
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

    script_type = forms.ModelChoiceField(
            label="Script Type*",
            queryset=ScriptType.objects.filter(enabled=True),
            empty_label="--None--",
            required=True,
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

    script_category = forms.ModelChoiceField(
        label="Script Category*",
        queryset=ScriptCategory.objects.filter(enabled=True),
        empty_label="--None--",
        required=True,
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
        fields = ("user", "name", "version", "type", "script_type", "script_category", "code", "fileRef", "description")
        model = Automation
        labels = {
            "description": "Description*",
            "fileRef": "Attachment",
            'name': 'Name*',
            'version': 'Version*',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'size': 50,
                'style': 'width:50%',
                'class': 'form-control'}
            ),
            'version': forms.TextInput(attrs={
                'size': 20,
                'style': 'width:50%',
                'class': 'form-control'}
            ),
            'code': forms.Textarea(attrs={
                'size': 20,
                'style': 'width:50%',
                'class': 'form-control'}
            ),
            # 'fileRef': CustomClearableFileInput,
            'description': TinyMCEWidget(
                mce_attrs={
                    'width': '90%',

                    # 'readonly': True,
                    # 'menubar': False,
                    # 'toolbar': False,
                    #                    'autoresize_overflow_padding': 10,

                },
                attrs={
                    'style': 'padding-right: 100px',
                }
            ),
        }

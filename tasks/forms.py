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
# 2019.11.17  Lendvay     1      Fixed the playbooktemplates
# 2020.02.15  Lendvay     1      Fixed dropdown colors
# **********************************************************************;
from django import forms
# from django.db.models import Count, Avg, Min, Max, Sum, F
from django.db.models import Max
from invs.widgets import JQueryDateTimePickerInput
from tinymce import TinyMCE
from .models import Task, TaskCategory, TaskPriority, TaskStatus, TaskTemplate, TaskType, TaskVar, TaskVarCategory, \
    TaskVarType, Type, EvidenceFormat, EvidenceAttrFormat, EvidenceAttr, Evidence, EvReputation, \
    Action, ActionGroup, ActionGroupMember, Playbook, PlaybookTemplate, PlaybookTemplateItem, \
    ScriptType, ScriptOutput, ScriptCategory, ScriptInput, OutputTarget,\
    Inv, MitreAttck_Tactics, Automation
from assets.models import Host, Hostname, Ipaddress, Profile
from configuration.models import ConnectionItem
# from django.core.exceptions import ValidationError
# Get the user so we can use this
from django.contrib.auth import get_user_model
import logging
User = get_user_model()
logger = logging.getLogger('log_file_verbose')


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


# the forms generate too many DB queries, this class is to replace db queries with a list
# https://stackoverflow.com/questions/32082945/django-multiple-forms-with-modelchoicefield-too-many-queries
class ListModelChoiceField(forms.ChoiceField):
    """
    special field using list instead of queryset as choices
    """
    def __init__(self, model, *args, **kwargs):
        self.model = model
        super(ListModelChoiceField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value in self.empty_values:
            return None
        try:
            value = self.model.objects.get(id=value)
        except self.model.DoesNotExist:
             # XXXXXX(self.error_messages['invalid_choice'], code='invalid_choice')
            print("Wrong Model Name")
        return value


    def valid_value(self, value):
        "Check to see if the provided value is a valid choice"
        # if self.choices[0][0] == "":
        #     return True
        if any(choice[0] == "" or value.id == int(choice[0]) for choice in self.choices):
            return True
        # if any(value.id == int(choice[0]) for choice in self.choices):
        #     return True
        return False

    def to_choicelist(self):
        value = None
        if value in self.empty_values:
            return None
        try:
            value = self.model.objects.all()
        except self.model.DoesNotExist:
             # XXXXXX(self.error_messages['invalid_choice'], code='invalid_choice')
            print("Wrong Model Name")
            value = self.model.objects.none()
        return value

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
                'data-style': 'btn-outline-secondary btn-sm',
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
                'data-style': 'btn-outline-secondary btn-sm',
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
                'data-style': 'btn-outline-secondary btn-sm',
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
                'data-style': 'btn-outline-secondary btn-sm',
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
                'data-style': 'btn-outline-secondary btn-sm',
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
                'data-style': 'btn-outline-secondary btn-sm',
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
                'data-style': 'btn-outline-secondary btn-sm',
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
                'data-style': 'btn-outline-secondary btn-sm',
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
                'data-style': 'btn-outline-secondary btn-sm',
                'style': 'width:50%',
            }
        )
    )

    #   fileRef = forms.FileField(widget=CustomClearableFileInput)
    class Meta:
        fields = ("user", "title", "version", "enabled", "automationid", "scriptinput", "scriptinputattrtype",
                  "runonsaveattr", "skipregex", "reputationregex", "intelfeed", "scriptinputattrtypeall", "scriptoutput",  "scriptoutputtype", "outputtarget",
                  "outputdescformat", "argument", "connectionitemid", "timeout", "fileRef", "description")
        model = Action
        labels = {
            "description": "Description*",
            "fileRef": "Attachment",
            'argument': 'Argument (parameters: $FILE$, $EVIDENCE$, $OUTDIR$',
            "timeout": "Timeout (sec)",
            'title': 'Title*',
            'version': 'Version*',
            'scriptoutput': 'Script output format',
            'outputtarget': 'Output Target*',
            'runonsaveattr': 'Run when saving attribute type',
            'skipregex': 'Regex to skip when running on save',
            'reputationregex': 'Regex to filter for reputation',
            'intelfeed': 'Intelligence Feed',
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
            'skipregex': forms.TextInput(attrs={
                'size': 255,
                'style': 'width:50%',
                'class': 'form-control'}
            ),
            'reputationregex': forms.TextInput(attrs={
                'size': 255,
                'style': 'width:50%',
                'class': 'form-control'}
            ),
            'argument': forms.Textarea(attrs={
                'rows': '1',
                'cols': '25',
                'style': 'width:90%',
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
                'data-style': 'btn-outline-secondary btn-sm',
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
                'data-style': 'btn-outline-secondary btn-sm',
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
        invlist = kwargs.pop("invlist", None)
        taskstatuslist = kwargs.pop("taskstatuslist", None)
        actiontargetlist = kwargs.pop("actiontargetlist", None)
        actionlist = kwargs.pop("actionlist", None)
        parentlist = kwargs.pop("parentlist", None)
        inputfromlist = kwargs.pop("inputfromlist", None)
        super(TaskForm, self).__init__(*args, **kwargs)
        logger.info("TaskForm - "+str(user))
        # self.fields['inv'].initial = inv_pk
        # if kwargs.get('instance'):
        #     curr_obj = kwargs.get('instance')
        #     current_pk = curr_obj.pk
        #     if inv_pk and inv_pk != '0' and inv_pk != 0:
        #         inv_obj = Inv.objects.get(pk=inv_pk)
        #         self.fields['parent'].queryset = inv_obj.task_inv.exclude(pk=current_pk)
        #         self.fields['inputfrom'].queryset = inv_obj.task_inv.exclude(pk=current_pk)
        #     elif inv_pk != '0' and inv_pk != 0:
        #         inv_obj = curr_obj.inv
        #         self.fields['parent'].queryset = inv_obj.task_inv.exclude(pk=current_pk)
        #         self.fields['inputfrom'].queryset = inv_obj.task_inv.exclude(pk=current_pk)
        #     else:
        #         self.fields['parent'].queryset = Task.objects.all()
        #         self.fields['inputfrom'].queryset = Task.objects.all()
        #
        # elif inv_pk and inv_pk != '0' and inv_pk != 0:
        #     inv_obj = Inv.objects.get(pk=inv_pk)
        #     self.fields['parent'].queryset = inv_obj.task_inv.all()
        #     self.fields['inputfrom'].queryset = inv_obj.task_inv.all()
        # else:
        #     self.fields['parent'].queryset = Task.objects.filter(pk=0)
        #     self.fields['inputfrom'].queryset = Task.objects.filter(pk=0)
        self.fields['user'].initial = user
        self.fields['status'].initial = 3
        self.fields['priority'].initial = 1
        self.fields['status'] = ListModelChoiceField(TaskStatus,
                                                  choices=taskstatuslist,
                                                  label='Status*',
                                                  # empty_label="--Select--",
                                                  # queryset overwritten above
                                                  # queryset=Inv.objects.all(),
                                                  required=False,
                                                  initial=inv_pk,
                                                  widget=forms.Select(
                                                      attrs={
                                                          'class': 'selectpicker show-tick form-control',  # form-control
                                                          'data-live-search': 'true',
                                                          'data-width': 'auto',
                                                          'data-style': 'btn-secondary btn-sm',
                                                          'style': 'width:50%',
                                                      }
                                                  )
                                                  )
        self.fields['inv'] = ListModelChoiceField(Inv,
                                                  choices=invlist,
                                                  label='Investigation',
                                                  # empty_label="--Select--",
                                                  # queryset overwritten above
                                                  # queryset=Inv.objects.all(),
                                                  required=False,
                                                  initial=inv_pk,
                                                  widget=forms.Select(
                                                      attrs={
                                                          'class': 'selectpicker show-tick form-control',  # form-control
                                                          'data-live-search': 'true',
                                                          'data-width': 'auto',
                                                          'data-style': 'btn-outline-secondary btn-sm',
                                                          'style': 'width:50%',
                                                      }
                                                  )
                                                  )
        self.fields['actiontarget'] = ListModelChoiceField(Task,
                                                  choices=actiontargetlist,
                                                  label='Action Target Task',
                                                  # empty_label="--Select--",
                                                  # queryset overwritten above
                                                  # queryset=Inv.objects.all(),
                                                  required=False,
                                                  # initial=,
                                                  widget=forms.Select(
                                                      attrs={
                                                          'class': 'selectpicker show-tick form-control',  # form-control
                                                          'data-live-search': 'true',
                                                          'data-width': 'auto',
                                                          'data-style': 'btn-outline-secondary btn-sm',
                                                          'style': 'width:50%',
                                                      }
                                                  )
                                                  )

        self.fields['action'] = ListModelChoiceField(Action,
                                                  choices=actionlist,
                                                  label='Action',
                                                  # empty_label="--Select--",
                                                  # queryset overwritten above
                                                  # queryset=Inv.objects.all(),
                                                  required=False,
                                                  # initial=,
                                                  widget=forms.Select(
                                                      attrs={
                                                          'class': 'selectpicker show-tick form-control',  # form-control
                                                          'data-live-search': 'true',
                                                          'data-width': 'auto',
                                                          'data-style': 'btn-outline-secondary btn-sm',
                                                          'style': 'width:50%',
                                                      }
                                                  )
                                                  )

        self.fields['parent'] = ListModelChoiceField(Task,
                                                  choices=parentlist,
                                                  label='Parent Task',
                                                  # empty_label="--Select--",
                                                  # queryset overwritten above
                                                  # queryset=Inv.objects.all(),
                                                  required=False,
                                                  # initial=,
                                                  widget=forms.Select(
                                                      attrs={
                                                          'class': 'selectpicker show-tick form-control',  # form-control
                                                          'data-live-search': 'true',
                                                          'data-width': 'auto',
                                                          'data-style': 'btn-outline-secondary btn-sm',
                                                          'style': 'width:50%',
                                                      }
                                                  )
                                                  )
        self.fields['inputfrom'] = ListModelChoiceField(Task,
                                                  choices=inputfromlist,
                                                  label='Input Task',
                                                  # empty_label="--Select--",
                                                  # queryset overwritten above
                                                  # queryset=Inv.objects.all(),
                                                  required=False,
                                                  # initial=,
                                                  widget=forms.Select(
                                                      attrs={
                                                          'class': 'selectpicker show-tick form-control',  # form-control
                                                          'data-live-search': 'true',
                                                          'data-width': 'auto',
                                                          'data-style': 'btn-outline-secondary btn-sm',
                                                          'style': 'width:50%',
                                                      }
                                                  )
                                                  )


    # status = forms.ModelChoiceField(
    #     label='Status*',
    #     queryset=TaskStatus.objects.filter(enabled=True),
    #     empty_label="--Select--",
    #     widget=forms.Select(
    #         attrs={
    #             'class': 'selectpicker show-tick form-control',  # form-control
    #             'data-live-search': 'true',
    #             'data-width': 'auto',
    #             'data-style': 'btn-secondary btn-sm',
    #             'style': 'width:50%',
    #         }
    #     )
    # )

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
                'data-style': 'btn-outline-secondary btn-sm',
                'style': 'width:50%',
            }
        )
    )

    # action = forms.ModelChoiceField(
    #     label='Action',
    #     #  queryset overwritten in init
    #     queryset=Action.objects.filter(enabled=True),
    #     required=False,
    #     empty_label="--Select--",
    #     widget=forms.Select(
    #         attrs={
    #             'class': 'selectpicker show-tick form-control',  # form-control
    #             'data-live-search': 'true',
    #             'data-width': 'auto',
    #             'data-style': 'btn-outline-secondary btn-sm',
    #             'style': 'width:50%',
    #         }
    #     )
    # )

    # actiontarget = forms.ModelChoiceField(
    #     label='Action Target Task',
    #     #  queryset overwritten in init
    #     queryset=Task.objects.all(),
    #     required=False,
    #     empty_label="--Select--",
    #     widget=forms.Select(
    #         attrs={
    #             'class': 'selectpicker show-tick form-control',  # form-control
    #             'data-live-search': 'true',
    #             'data-width': 'auto',
    #             'data-style': 'btn-outline-secondary btn-sm',
    #             'style': 'width:50%',
    #         }
    #     )
    # )

    # parent = forms.ModelChoiceField(
    #     label='Parent',
    #     #  queryset overwritten in init
    #     queryset=Task.objects.all(),
    #     required=False,
    #     empty_label="--Select--",
    #     widget=forms.Select(
    #         attrs={
    #             'class': 'selectpicker show-tick form-control',  # form-control
    #             'data-live-search': 'true',
    #             'data-width': 'auto',
    #             'data-style': 'btn-outline-secondary btn-sm',
    #             'style': 'width:50%',
    #         }
    #     )
    # )
    #
    # inputfrom = forms.ModelChoiceField(
    #     label='Input Task',
    #     #  queryset overwritten in init
    #     queryset=Task.objects.all(),
    #     required=False,
    #     empty_label="--Select--",
    #     widget=forms.Select(
    #         attrs={
    #             'class': 'selectpicker show-tick form-control',  # form-control
    #             'data-live-search': 'true',
    #             'data-width': 'auto',
    #             'data-style': 'btn-outline-secondary btn-sm',
    #             'style': 'width:50%',
    #         }
    #     )
    # )

    # inv = forms.ModelChoiceField(
    #     label='Investigation',
    #     queryset=Inv.objects.exclude(status='2'),
    #     required=False,
    #     empty_label="--Select--",
    #     widget=forms.Select(
    #         attrs={
    #             'class': 'selectpicker show-tick form-control',  # form-control
    #             'data-live-search': 'true',
    #             'data-width': 'auto',
    #             'data-style': 'btn-outline-secondary btn-sm',
    #             'style': 'width:50%',
    #         }
    #     )
    # )

    category = forms.ModelChoiceField(
        label='Category*',
        queryset=TaskCategory.objects.filter(enabled=True),
        empty_label="--Select--",
        widget=forms.Select(
            attrs={
                'class': 'selectpicker show-tick form-control',  # form-control
                'data-live-search': 'true',
                'data-width': 'auto',
                'data-style': 'btn-secondary btn-sm',
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
                'data-style': 'btn-secondary btn-sm',
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
                'data-style': 'btn-secondary btn-sm',
                'style': 'width:50%',
            }
        )
    )

    # starttime = forms.SplitDateTimeField(
    #     required=False,
    #     label='Start of task',
    #     input_date_formats=['%m/%d/%Y'],
    #     input_time_formats=['%H:%M'],
    #     widget=SplitDateTimeWidget(
    #         date_format='%m/%d/%Y',
    #         time_format='%H:%M',
    #         attrs={
    #             'class': 'form-control',
    #             'style': 'width:100px',
    #         }
    #     )
    # )
    starttime = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:%M:%S'],
        required=False,
        widget=JQueryDateTimePickerInput(
            attrs={
                'class': 'form-control',
                'style': 'width:200px',
            }
        )
    )
    # endtime = forms.SplitDateTimeField(
    #     required=False,
    #     label='End of task',
    #     input_date_formats=['%m/%d/%Y'],
    #     input_time_formats=['%H:%M'],
    #     widget=SplitDateTimeWidget(
    #         date_format='%m/%d/%Y',
    #         time_format='%H:%M',
    #         attrs={
    #             'class': 'form-control',
    #             'style': 'width:100px',
    #         }
    #     )
    # )
    endtime = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:%M:%S'],
        required=False,
        widget=JQueryDateTimePickerInput(
            attrs={
                'class': 'form-control',
                'style': 'width:200px',
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
                  'requiresevidence',
                  'starttime',
                  'endtime')
        labels = {
            'title': 'Title*',
            'user': "Assigned to",
            'summary': "Summary",
            'description': 'Description*',
            'requiresevidence': 'Requires evidence*'
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
        self.fields['status'].initial = 3
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
                'data-style': 'btn-secondary btn-sm',
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
                'data-style': 'btn-outline-secondary btn-sm',
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
                'data-style': 'btn-outline-secondary btn-sm',
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
                'data-style': 'btn-outline-secondary btn-sm',
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
                'data-style': 'btn-secondary btn-sm',
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
                'data-style': 'btn-secondary btn-sm',
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
                'data-style': 'btn-secondary btn-sm',
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
                  'requiresevidence',
                  )
        labels = {
            'tasktemplatename': "Template Name*",
            'user': "Assigned to",
            'summary': "Summary",
            'description': 'Description*',
            'requiresevidence': 'Requires evidence*',
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
        required=False,
        empty_label="--Select--",
        widget=forms.Select(
            attrs={
                'class': 'selectpicker show-tick form-control',  # form-control
                'data-live-search': 'true',
                'data-width': 'auto',
                'data-style': 'btn-outline-secondary btn-sm',
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
                'data-style': 'btn-outline-secondary btn-sm',
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
                'data-style': 'btn-outline-secondary btn-sm',
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
                'data-style': 'btn-outline-secondary btn-sm',
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
                'data-style': 'btn-outline-secondary btn-sm',
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
                'data-style': 'btn-outline-secondary btn-sm',
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
                'data-style': 'btn-outline-secondary btn-sm',
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
                'data-style': 'btn-outline-secondary btn-sm',
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
        if PlaybookTemplateItem.objects.filter(playbooktemplateid=self.play_pk):
            self.fields['itemorder'].initial = int(PlaybookTemplateItem.objects.
                                                   filter(playbooktemplateid=self.play_pk).
                                                   aggregate(Max('itemorder'))['itemorder__max'])+1
        else:
            self.fields['itemorder'].initial = 100
        # This means that we are editing
        if kwargs.get('instance'):
            currentitem_pk = kwargs.get('instance').pk

            # print("EDIT: %s %s"%(currentitem_pk,type(currentitem_pk)))
            if currentitem_pk:
                try:
                    if PlaybookTemplateItem.objects.filter(pk=currentitem_pk):
                        actual_playbooktemplateitem_obj = PlaybookTemplateItem.objects.get(pk=currentitem_pk)
                        actual_playbook_obj = actual_playbooktemplateitem_obj.playbooktemplateid
                        prevtask = actual_playbook_obj.playbooktemplateitem_playbooktemplate.\
                            filter(itemorder__lt=actual_playbooktemplateitem_obj.itemorder).exclude(pk=currentitem_pk)
                        # print(prevtask)
                        nexttask = actual_playbook_obj.playbooktemplateitem_playbooktemplate.\
                            exclude(pk=currentitem_pk)
                        # print(nexttask)
                        self.fields['prevtask'].queryset = prevtask
                        self.fields['nexttask'].queryset = nexttask
                except Exception:
                    self.fields['nexttask'].queryset = PlaybookTemplateItem.objects.all()
                    self.fields['prevtask'].queryset = PlaybookTemplateItem.objects.all()
                    pass

        # This means we are creating a new item
        else:
            if self.play_pk != "0" and self.play_pk is not None:
                try:
                    if PlaybookTemplateItem.objects.filter(playbooktemplateid__pk=self.play_pk).exists():
                        actual_playbooktemplate_obj = PlaybookTemplate.objects.get(pk=self.play_pk)
                        # actual_playbooktemplate = actual_playbooktemplate_obj.pk
                        actual_alltasks = actual_playbooktemplate_obj.playbooktemplateitem_playbooktemplate.all()
                        self.fields['nexttask'].queryset = actual_alltasks
                        self.fields['prevtask'].queryset = actual_alltasks
                    else:
                        self.fields['prevtask'].queryset = PlaybookTemplateItem.objects.none()
                        self.fields['nexttask'].queryset = PlaybookTemplateItem.objects.none()
                except Exception:
                    self.fields['prevtask'].queryset = PlaybookTemplateItem.objects.filter(enabled=True)
                    self.fields['nexttask'].queryset = PlaybookTemplateItem.objects.filter(enabled=True)
            else:
                self.fields['prevtask'].queryset = PlaybookTemplateItem.objects.filter(enabled=True)
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
                'data-style': 'btn-outline-secondary btn-sm',
                'style': 'width:50%',
            }
        )
    )

    playbooktemplateid = forms.ModelChoiceField(
        label='PlaybookTemplate*',
        queryset=PlaybookTemplate.objects.filter(enabled=True),
        empty_label="--Select--",
        disabled=True,
        widget=forms.Select(
            attrs={
                'class': 'selectpicker show-tick form-control',  # form-control
                'data-live-search': 'true',
                'data-width': 'auto',
                'data-style': 'btn-outline-secondary btn-sm',
                'style': 'width:50%',
            }
        )
    )

    prevtask = forms.ModelChoiceField(
            label="Previous Task",
            queryset=None,  # TaskTemplate.objects.filter(enabled=True),
            # the line above is overriden by the __INIT__ only allow available tasks
            empty_label="--None--",
            required=False,
            widget=forms.Select(
                attrs={
                    'class': 'selectpicker show-tick form-control',  # form-control
                    'data-live-search': 'true',
                    'data-width': 'auto',
                    'data-style': 'btn-outline-secondary btn-sm',
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
                'data-style': 'btn-outline-secondary btn-sm',
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
                    'data-style': 'btn-outline-secondary btn-sm',
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
                'data-style': 'btn-outline-secondary btn-sm',
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


# class CustomClearableFileInput(ClearableFileInput):
#     template_name = 'invs/customclearablefileinput.html'
class EvidenceForm(forms.ModelForm):
    # inv_pk and task_pk defaults to zero as they are not needed for updates
    # evidenceformat=2
    def __init__(self, inv_pk=0, task_pk=0, *args, **kwargs):
        user = kwargs.pop("user", None)
        invlist = kwargs.pop("invlist", None)
        tasklist = kwargs.pop("tasklist", None)
        # inv_pk = kwargs.pop("inv_pk", None)
        # task_pk = kwargs.pop("task_pk", None)
        super(EvidenceForm, self).__init__(*args, **kwargs)
        logger.info("EvidenceForm - "+str(user))
        self.fields['user'].initial = user
        # self.fields['inv'].initial = inv_pk
        self.fields['inv'] = ListModelChoiceField(Inv,
                                                  choices=invlist,
                                                  label='Related Investigation',
                                                  # empty_label="--Select--",
                                                  # queryset overwritten above
                                                  # queryset=Inv.objects.all(),
                                                  required=False,
                                                  initial=inv_pk,
                                                  widget=forms.Select(
                                                      attrs={
                                                          'class': 'selectpicker show-tick form-control',  # form-control
                                                          'data-live-search': 'true',
                                                          'data-width': 'auto',
                                                          'data-style': 'btn-secondary btn-sm',
                                                          'style': 'width:50%',
                                                      }
                                                  )
                                                  )
        # self.fields['task'].initial = task_pk
        self.fields['task'] = ListModelChoiceField(Task,
                                                   choices=tasklist,
                                                   label='Related Task',
                                                   # empty_label="--Select--",
                                                   # queryset overwritten above
                                                   # queryset=Inv.objects.all(),
                                                   initial=task_pk,
                                                   required=False,
                                                   widget=forms.Select(
                                                       attrs={
                                                           'class': 'selectpicker show-tick form-control',  # form-control
                                                           'data-live-search': 'true',
                                                           'data-width': 'auto',
                                                           'data-style': 'btn-secondary btn-sm',
                                                           'style': 'width:50%',
                                                       }
                                                   )

                                                   )

###############
        # if kwargs.get('instance'):
        #     curr_obj = kwargs.get('instance')
        #     current_pk = curr_obj.pk
        #     if inv_pk:
        #         inv_obj = Inv.objects.get(pk=inv_pk)
        #     else:
        #         inv_obj = curr_obj.inv
        #     if inv_obj:
        #         self.fields['task'].queryset = inv_obj.task_inv.exclude(pk=current_pk).select_related('status')
        #     else:
        #         self.fields['task'].queryset = Task.objects.all().select_related('status')
        #
        # elif inv_pk == '0' or inv_pk == 0:
        #     self.fields['task'].queryset = Task.objects.all().select_related('status')
        # else:
        #     inv_obj = Inv.objects.get(pk=inv_pk)
        #     self.fields['task'].queryset = inv_obj.task_inv.all().select_related('status')
        #     self.fields['task'].queryset = Task.objects.all()

###############
        if EvidenceFormat.objects.get(pk=2):
            self.fields['evidenceformat'].initial = EvidenceFormat.objects.get(pk=2)
        # if kwargs.get('instance'):
        #     current_pk = kwargs.get('instance').pk
        #     self.evidenceformat=Evidence.objects.get(pk=current_pk).evidenceformat

    user = forms.ModelChoiceField(
        label='Owner*',
        queryset=User.objects.filter(is_active=True),
        empty_label="--Select--",
        widget=forms.Select(
            attrs={
                'class': 'selectpicker show-tick form-control',  # form-control
                'data-live-search': 'true',
                'data-width': 'auto',
                'data-style': 'btn-outline-secondary btn-sm',
                'style': 'width:50%',
            }
        )
    )

    # inv = forms.ModelChoiceField(
    #     label="Related Investigation",
    #     # queryset=Inv.objects.exclude(status='2'),  # CLOSED
    #     queryset=Inv.objects.exclude(status=2).exclude(status=4),
    #     empty_label="--None--",
    #     required=False,
    #     widget=forms.Select(
    #         attrs={
    #             'class': 'selectpicker show-tick form-control',  # form-control
    #             'data-live-search': 'true',
    #             'data-width': 'auto',
    #             'data-style': 'btn-secondary btn-sm',
    #             'style': 'width:50%',
    #         }
    #     )
    # )
    #
    # task = forms.ModelChoiceField(
    #     label="Related Task",
    #     # queryset=Task.objects.exclude(status='2'),  #  exclude closed task
    #     queryset=Task.objects.none(),
    #     empty_label="--None--",
    #     required=False,
    #     widget=forms.Select(
    #         attrs={
    #             'class': 'selectpicker show-tick form-control',  # form-control
    #             'data-live-search': 'true',
    #             'data-width': 'auto',
    #             'data-style': 'btn-secondary btn-sm',
    #             'style': 'width:50%',
    #         }
    #     )
    # )

    parent = forms.ModelChoiceField(
        label='Parent',
        queryset=Evidence.objects.all(), # todo exclude itself
        empty_label="--Select--",
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'selectpicker show-tick form-control',  # form-control
                'data-live-search': 'true',
                'data-width': 'auto',
                'data-style': 'btn-outline-secondary btn-sm',
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
                'data-style': 'btn-secondary btn-sm',
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
                'data-style': 'btn-secondary btn-sm',
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
                'data-style': 'btn-outline-secondary btn-sm',
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
                'data-style': 'btn-outline-secondary btn-sm',
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
                'data-style': 'btn-outline-secondary btn-sm',
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
                'data-style': 'btn-outline-secondary btn-sm',
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
                    'class': 'form-check',
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
                'data-style': 'btn-outline-secondary btn-sm',
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
                'data-style': 'btn-outline-secondary btn-sm',
                'style': 'width:50%',
            }
        )
    )

    # max_number = forms.ChoiceField(widget=forms.Select(),
    #                                choices=([('check_malicious', 'check_malicious'),
    #                                          ('find_ipv4', 'find_ipv4'), ('3', '3'), ]), initial='1', required=True, )

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
                    'data-style': 'btn-outline-secondary btn-sm',
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
                'data-style': 'btn-outline-secondary btn-sm',
                'style': 'width:50%',
            }
        )
    )

    #   fileRef = forms.FileField(widget=CustomClearableFileInput)
    class Meta:
        fields = ("user", "name", "version", "type", "script_type", "script_category", "code", "autorequirements",
                  "fileRef", "description")
        model = Automation
        labels = {
            "description": "Description*",
            "autorequirements": "Software reuqirements",
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
                'style': 'width:90%;min-height:500px',
                'class': 'form-control'}
            ),
            'autorequirements': forms.Textarea(attrs={
                'size': 20,
                'style': 'width:90%',
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


# Add a ticket to the Task and close the task
class AddTicketAndCloseForm(forms.Form):
    ticket = forms.CharField(
        label='Ticket*',
        max_length=50,
        widget=forms.TextInput(attrs={
            'size': 20,
            'style': 'width:50%;',
            'class': 'form-control'}
        )
    )
    status = forms.ModelChoiceField(
        label='Status*',
        queryset=TaskStatus.objects.filter(enabled=True),
        empty_label="--Select--",
        initial=5,
        widget=forms.Select(
            attrs={
                'class': 'selectpicker show-tick form-control',  # form-control
                'data-live-search': 'true',
                'data-width': 'auto',
                'data-style': 'btn-outline-secondary btn-sm',
                'style': 'width:50%',
            }
        )
    )

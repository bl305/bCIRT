# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : knowledgebase/forms.py
# Author            : Balazs Lendvay
# Date created      : 2020.03.29
# Purpose           : Forms file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2020.03.29  Lendvay     1      Initial file
# **********************************************************************;
from django import forms
# from django.db.models import Count, Avg, Min, Max, Sum, F
from django.db.models import Max
from invs.widgets import JQueryDateTimePickerInput
from tinymce import TinyMCE
from .models import KnowledgeBase, KnowledgeBaseFormat
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


class KnowledgeBaseForm(forms.ModelForm):
    # evidenceformat=2
    def __init__(self, kb_pk=0, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(KnowledgeBaseForm, self).__init__(*args, **kwargs)
        logger.info("KnwoledgeBaseForm - "+str(user))
        # self.fields['inv'].initial = inv_pk
        # parentlist = kwargs.pop("parentlist", None)
        # self.fields['parent'].queryset = KnowledgeBase.objects.exclude(pk=kb_pk)
        # self.fields['parent'] = ListModelChoiceField(KnowledgeBase,
        #                                           choices=parentlist,
        #                                           label='Parent KB Article',
        #                                           # empty_label="--Select--",
        #                                           # queryset overwritten above
        #                                           # queryset=Inv.objects.all(),
        #                                           required=False,
        #                                           # initial=,
        #                                           widget=forms.Select(
        #                                               attrs={
        #                                                   'class': 'selectpicker show-tick form-control',  # form-control
        #                                                   'data-live-search': 'true',
        #                                                   'data-width': 'auto',
        #                                                   'data-style': 'btn-outline-secondary btn-sm',
        #                                                   'style': 'width:50%',
        #                                               }
        #                                           )
        #                                           )        # self.fields['task'].initial = task_pk
        if KnowledgeBaseFormat.objects.get(pk=2):
            self.fields['knowledgebaseformat'].initial = KnowledgeBaseFormat.objects.get(pk=2)

    # parent = forms.ModelChoiceField(
    #     label='Parent',
    #     queryset=KnowledgeBase.objects.all(),
    #     empty_label="--Select--",
    #     required=False,
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

    knowledgebaseformat = forms.ModelChoiceField(
        label="KB format*",
        queryset=KnowledgeBaseFormat.objects.filter(enabled=True),  # .values_list('name',flat=True),
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


    class Meta:
        fields = ("id", "enabled", "title", "knowledgebaseformat", "description", "fileRef")
        model = KnowledgeBase
        labels = {
            # "parent": "Parent",
            "kbformat": "KB format",
            "description": "Description*",
            "fileRef": "Attachment",
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'size': 50,
                'style': 'width:50%;',
                'class': 'form-control'}
            ),
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

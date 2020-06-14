# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : invs/forms.py
# Author            : Balazs Lendvay
# Date created      : 2019.07.27
# Purpose           : Forms file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.07.29  Lendvay     1      Initial file
# 2020.06.13  Lendvay     2      Autofocus
# **********************************************************************;
from .widgets import JQueryDateTimePickerInput

from django import forms
from .models import Inv, InvStatus, InvSeverity, InvPhase, InvCategory, InvAttackVector, InvPriority, \
    CurrencyType, InvReviewRules
import logging
from tinymce import TinyMCE
# Get the user so we can use this
from django.contrib.auth import get_user_model
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

        if any(choice[0] == "" or value.id == int(choice[0]) for choice in self.choices):
            return True
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
class InvForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        # pparent is needed to replace the X query i nthe form, "x" being the number of investigations
        pparent = kwargs.pop("pparent", None)

        super(InvForm, self).__init__(*args, **kwargs)
        logger.info("InvForm - "+str(user))

        # if kwargs.get('instance'):
        #     current_pk = kwargs.get('instance').pk
        #     self.fields['parent'].queryset = Inv.objects.all().exclude(pk=current_pk)
        # else:
        #     self.fields['parent'].queryset = Inv.objects.all()
        self.fields['user'].initial = user
        self.fields['status'].initial = 3
        self.fields['phase'].initial = 1
        self.fields['severity'].initial = 2
        self.fields['priority'].initial = 1
        self.fields['losscurrency'].initial = 1
        self.fields['numofvictims'].initial = None
        self.fields['parent'] = ListModelChoiceField(Inv,
                                                     choices=pparent,
                                                     label='Parent',
                                                     # empty_label="--Select--",
                                                     # queryset overwritten above
                                                     # queryset=Inv.objects.all(),
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

    status = forms.ModelChoiceField(
        label='Status*',
        queryset=InvStatus.objects.filter(enabled=True).exclude(name="Review2").exclude(name="Closed").
            exclude(name="Archived").order_by('name'),
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



    # parent = forms.ModelChoiceField(
    #     label='Parent',
    #     empty_label="--Select--",
    #     # queryset overwritten above
    #     queryset=Inv.objects.all(),
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

    phase = forms.ModelChoiceField(
        label='Phase*',
        queryset=InvPhase.objects.filter(enabled=True),
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

    severity = forms.ModelChoiceField(
        label='Severity*',
        queryset=InvSeverity.objects.filter(enabled=True),
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

    category = forms.ModelChoiceField(
        label='Category*',
        queryset=InvCategory.objects.filter(enabled=True),
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
        queryset=InvPriority.objects.filter(enabled=True),
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

    attackvector = forms.ModelChoiceField(
        label='Attack vector*',
        queryset=InvAttackVector.objects.filter(enabled=True),
        empty_label="--Select--",
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

    losscurrency = forms.ModelChoiceField(
        label='Currency*',
        queryset=CurrencyType.objects.filter(enabled=True),
        empty_label="--Select--",
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'selectpicker show-tick form-control',  # form-control
                'data-live-search': 'true',
                'data-width': 'auto',
                'data-style': 'btn-secondary btn-sm',
                'style': 'width:30%',
            }
        )
    )

    incstarttime = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:%M:%S'],
        required=False,
        widget=JQueryDateTimePickerInput(
            attrs={
                'class': 'form-control',
                'style': 'width:200px',
            }
        )
    )

    incendtime = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:%M:%S'],
        required=False,
        widget=JQueryDateTimePickerInput(
            attrs={
                'class': 'form-control',
                'style': 'width:200px',
            }
        )
    )

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

    # attrs = {
    #     'class': 'form-control',
    #     'style': 'width:100px',
    # }

    class Meta:
        model = Inv
        fields = ('invid',
                  'ticketid',
                  'refid',
                  'status',
                  'priority',
                  'description',
                  'summary',
                  'user',
                  'parent',
                  'phase',
                  'severity',
                  'category',
                  'attackvector',
                  'comment',
                  'numofvictims',
                  'potentialloss',
                  'monetaryloss',
                  'losscurrency',
                  'incstarttime',
                  'incendtime',
                  'starttime',
                  'endtime',
                  'processimprovement')
        labels = {
            'invid': "Investigation",
            'ticketid': "Ticket#",
            'refid': "Reference",
            'user': "Assigned to",
            'description': 'Incident Description*',
            'summary': "Executive Summary",
            'comment': "Attack Comment",
            'potentialloss': "Potential Loss",
            'monetaryloss': "Monetary Loss",
            'losscurrency': "Currency",
            'numofvictims': "Victim Count:",
            'processimprovement': "Process Improvement"
        }
        widgets = {
            'invid': forms.TextInput(attrs={
                'autofocus': 'autofocus',
                'size': 20,
                'style': 'width:50%;',
                'class': 'form-control'}
            ),
            'ticketid': forms.TextInput(attrs={
                'size': 20,
                'style': 'width:50%;',
                'class': 'form-control'}
            ),
            'refid': forms.TextInput(attrs={
                'size': 20,
                'style': 'width:50%;',
                'class': 'form-control'}
            ),
            # 'description': forms.Textarea(attrs={
            #     'rows': '5',
            #     'cols': '68',
            #     'style': 'width:90%',
            #     'class': 'form-control'}
            # ),
            'description': TinyMCEWidget(
                mce_attrs={
                    'width': '95%',
                },
                attrs={
                    'style': 'padding-right: 100px',
                }
            ),
            # 'processimprovement': forms.Textarea(attrs={
            #     'rows': '5',
            #     'cols': '68',
            #     'style': 'width:90%',
            #     'class': 'form-control'}
            # ),
            # 'processimprovement': TinyMCEWidget(
            #     mce_attrs={
            #         'width': '95%',
            #     },
            #     attrs={
            #         'style': 'padding-right: 100px',
            #     }
            # ),
            # 'summary': forms.Textarea(attrs={
            #     'rows': '5',
            #     'cols': '68',
            #     'style': 'width:90%',
            #     'class': 'form-control'}
            # ),
            # 'summary': TinyMCEWidget(
            #     mce_attrs={
            #         'width': '95%',
            #     },
            #     attrs={
            #         'style': 'padding-right: 100px',
            #     }
            # ),
            'comment': forms.TextInput(attrs={
                'size': 50,
                'style': 'width:50%',
                'class': 'form-control'}
            ),
            'numofvictims': forms.NumberInput(attrs={
                'size': 20,
                'style': 'width:20%',
                'class': 'form-control'}
            ),
            'potentialloss': forms.NumberInput(attrs={
                'size': 20,
                'style': 'width:20%',
                'class': 'form-control'}
            ),
            'monetaryloss': forms.NumberInput(attrs={
                'size': 20,
                'style': 'width:20%',
                'class': 'form-control'}
            ),
            'losscurrency': forms.TextInput(attrs={
                'size': 20,
                'style': 'width:50%;',
                'class': 'form-control'}
            ),
        }


class InvReviewRulesForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)

        super(InvReviewRulesForm, self).__init__(*args, **kwargs)
        logger.info("InvForm - "+str(user))

        if kwargs.get('instance'):
            current_pk = kwargs.get('instance').pk
            self.fields['parent'].queryset = Inv.objects.all().exclude(pk=current_pk)
        self.fields['user'].initial = user
        # self.fields['status'].initial = 3
        # self.fields['phase'].initial = 1
        # self.fields['severity'].initial = 2
        # self.fields['priority'].initial = 1
        # self.fields['losscurrency'].initial = 1
        # self.fields['numofvictims'].initial = None

    severity = forms.ModelChoiceField(
        label='Severity*',
        queryset=InvSeverity.objects.filter(enabled=True),
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

    category = forms.ModelChoiceField(
        label='Category*',
        queryset=InvCategory.objects.filter(enabled=True),
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
        queryset=InvPriority.objects.filter(enabled=True),
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

    attackvector = forms.ModelChoiceField(
        label='Attack vector*',
        queryset=InvAttackVector.objects.filter(enabled=True),
        empty_label="--Select--",
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

    class Meta:
        model = InvReviewRules
        fields = ('rulename',
                  'priority',
                  'severity',
                  'category',
                  'attackvector',
                  'potentialloss',
                  'monetaryloss',
                  )
        labels = {
            'rulename': "Rule Name",
            'potentialloss': "Potential Loss",
            'monetaryloss': "Monetary Loss",
        }
        widgets = {
            'rulename': forms.TextInput(attrs={
                'size': 50,
                'style': 'width:50%;',
                'class': 'form-control'}
            ),
            'potentialloss': forms.NumberInput(attrs={
                'size': 20,
                'style': 'width:20%',
                'class': 'form-control'}
            ),
            'monetaryloss': forms.NumberInput(attrs={
                'size': 20,
                'style': 'width:20%',
                'class': 'form-control'}
            ),
        }


class InvSuspiciousEmailForm(forms.Form):
    invid = forms.CharField(
        label='Investigation*',
        max_length=20,
        required=False,
        widget=forms.Textarea(attrs={
                'rows': '1',
                'cols': '48',
                'style': 'resize:none;width:90%',
                'class': 'form-control',
                'placeholder': 'Phishing',
                }
            )
    )
    description = forms.CharField(
        label='Investigation Description*',
        max_length=50,
        required=False,
        widget=forms.Textarea(attrs={
                'rows': '1',
                'cols': '48',
                'style': 'resize:none;width:90%',
                'class': 'form-control',
                'placeholder': 'Phishing',
                }
            )
    )
    ticket = forms.CharField(
        label='Ticket*',
        max_length=50,
        widget=forms.TextInput(attrs={
            'autofocus': 'autofocus',
            'size': 20,
            'style': 'width:50%;',
            'class': 'form-control'}
        )
    )
    reference = forms.CharField(
        label='Reference',
        required=False,
        max_length=50,
        widget=forms.TextInput(attrs={
            'size': 20,
            'style': 'width:50%;',
            'class': 'form-control'}
        )
    )
    fileRef = forms.FileField(label='Attachment*')


class InvReviewer1Form(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(InvReviewer1Form, self).__init__(*args, **kwargs)
        logger.info("InvReview1Form - "+str(user))

    class Meta:
        model = Inv
        fields = (
                  'reviewer1comment',
                  )
        labels = {
            'reviewer1comment': "Reviewer #1 Comments",
        }
        widgets = {
            # 'reviewer1comment': forms.Textarea(attrs={
            #     'rows': '5',
            #     'cols': '68',
            #     'style': 'width:90%',
            #     'class': 'form-control'}
            # ),
            'reviewer1comment': TinyMCEWidget(
                mce_attrs={
                    'width': '95%',
                },
                attrs={
                    'style': 'padding-right: 100px',
                }
            ),
        }


class InvReviewer2Form(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(InvReviewer2Form, self).__init__(*args, **kwargs)
        logger.info("InvReview2Form - "+str(user))

    class Meta:
        model = Inv
        fields = (
                  'reviewer2comment',
                  )
        labels = {
            'reviewer2comment': "Reviewer #2 Comments",
        }
        widgets = {
            # 'reviewer2comment': forms.Textarea(attrs={
            #     'rows': '5',
            #     'cols': '68',
            #     'style': 'width:90%',
            #     'class': 'form-control'}
            # ),
            'reviewer2comment': TinyMCEWidget(
                mce_attrs={
                    'width': '95%',
                },
                attrs={
                    'style': 'padding-right: 100px',
                }
            ),
        }

from django import forms
from .models import Inv, InvStatus, InvSeverity, InvPhase, InvCategory, InvAttackvector, InvPriority
import logging
from django.forms.widgets import SplitDateTimeWidget  # , ClearableFileInput
from tinymce import TinyMCE
# Get the user so we can use this
from django.contrib.auth import get_user_model
User = get_user_model()
logger = logging.getLogger('log_file_verbose')


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


# class CustomClearableFileInput(ClearableFileInput):
#     template_name = 'invs/customclearablefileinput.html'
class InvForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)

        super(InvForm, self).__init__(*args, **kwargs)
        logger.info("InvForm - "+str(user))
        self.fields['user'].initial = user
        self.fields['status'].initial = 3
        self.fields['severity'].initial = 2
        self.fields['priority'].initial = 1

    status = forms.ModelChoiceField(
        label='Status*',
        queryset=InvStatus.objects.filter(enabled=True).order_by('name'),
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

    parent = forms.ModelChoiceField(
        label='Parent',
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

    phase = forms.ModelChoiceField(
        label='Phase*',
        queryset=InvPhase.objects.filter(enabled=True),
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

    severity = forms.ModelChoiceField(
        label='Severity*',
        queryset=InvSeverity.objects.filter(enabled=True),
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
        queryset=InvCategory.objects.filter(enabled=True),
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
        queryset=InvPriority.objects.filter(enabled=True),
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

    attackvector = forms.ModelChoiceField(
        label='Attack vector',
        queryset=InvAttackvector.objects.filter(enabled=True),
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

    starttime = forms.SplitDateTimeField(
        required=False,
        label='Start of investigation',
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
        label='End of investigation',
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
        model = Inv
        fields = ('invid',
                  'status',
                  'description',
                  'summary',
                  'user',
                  'parent',
                  'phase',
                  'severity',
                  'category',
                  'priority',
                  'attackvector',
                  'comment',
                  'starttime',
                  'endtime')
        labels = {
            'invid': "Investigation ID*",
            'user': "Assigned to",
            'description': 'Incident Description*',
            'summary': "Executive Summary",
            'comment': "Attack Comment",
        }
        widgets = {
            'invid': forms.TextInput(attrs={
                'size': 20,
                'style': 'width:50%;',
                'class': 'form-control'}
            ),
            'description': forms.Textarea(attrs={
                'rows': '1',
                'cols': '48',
                'style': 'resize:none;width:90%',
                'class': 'form-control'}
            ),
            'summary': forms.Textarea(attrs={
                'rows': '5',
                'cols': '68',
                'style': 'width:90%',
                'class': 'form-control'}
            ),
            'comment': forms.TextInput(attrs={
                'size': 50,
                'style': 'width:50%',
                'class': 'form-control'}
            ),
        }

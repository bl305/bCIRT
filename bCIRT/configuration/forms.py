from django import forms
from tinymce import TinyMCE
from .models import UpdatePackage
# Get the user so we can use this
from django.contrib.auth import get_user_model
import logging
logger = logging.getLogger('log_file_verbose')
User = get_user_model()


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class UpdatePackageForm(forms.ModelForm):
    def __init__(self, conf_pk=0, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(UpdatePackageForm, self).__init__(*args, **kwargs)
        logger.info("UpdatePackageForm - "+str(user))
        self.fields['user'].initial = user

        # self.fields['conf_pk'].initial = conf_pk

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

    class Meta:
        fields = ("updateversion", "user", "description", "fileRef")
        model = UpdatePackage
        labels = {
            "updateversion": "Version*",
            "description": "Description*",
            "fileRef": "Attachment",
        }
        widgets = {
            'description': TinyMCEWidget(
                mce_attrs={
                    'width': '95%',
                },
                attrs={
                    'style': 'padding-right: 100px',
                }
            ),
            'updateversion': forms.TextInput(attrs={
                'size': 18,
                'style': 'width:50%;',
                'class': 'form-control'}
            ),

        }

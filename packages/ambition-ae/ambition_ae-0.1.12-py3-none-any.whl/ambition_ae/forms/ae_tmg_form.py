from django import forms
from edc_form_validators import FormValidatorMixin

from ..models import AeTmg
from ..form_validators import AeTmgFormValidator
from .modelform_mixin import ModelFormMixin


class AeTmgForm(FormValidatorMixin, ModelFormMixin, forms.ModelForm):

    form_validator_cls = AeTmgFormValidator

    action_identifier = forms.CharField(
        label='Action Identifier',
        required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = AeTmg
        fields = '__all__'

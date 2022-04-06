from django import forms
from django.forms import ModelForm
from .models import *

from django.utils.translation import gettext_lazy as _
from import_export.forms import ImportForm, ConfirmImportForm


class EventForm(ModelForm):
    class Meta:
        model = event
        fields = '__all__'


class MemberSheetUploadForm(forms.ModelForm):
    class Meta:
        model = MemberSheetUpload
        fields = ('description', 'document',)


class CustomImportForm(ImportForm):
    organization = forms.ModelChoiceField(
        queryset=Organization.objects.all(),
        required=True)


class CustomConfirmImportForm(ConfirmImportForm):

    organization = forms.ModelChoiceField(
        queryset=Organization.objects.all(),
        required=True)


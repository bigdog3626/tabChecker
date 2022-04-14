from cgitb import text
from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from import_export.forms import ImportForm, ConfirmImportForm
from django.forms.widgets import PasswordInput, TextInput


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


class CustomAuthenticationForm(AuthenticationForm):
    username=forms.CharField(widget=TextInput(attrs={'class':'validate','placeholder' : 'Email'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password'}))

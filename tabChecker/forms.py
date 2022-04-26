from cgitb import text
from django import forms
from django.forms import CharField, ModelForm
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from import_export.forms import ImportForm, ConfirmImportForm
from django.forms.widgets import PasswordInput, TextInput





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


class CreateEventForm(forms.ModelForm):
    event = forms.CharField(widget=TextInput(attrs={'placeholder':'Title'}), max_length=15, required=False)
    class Meta:
        model = Event
        fields = '__all__'

    


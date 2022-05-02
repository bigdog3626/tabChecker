from cgitb import text
from django import forms
from django.forms import CharField, ModelForm, SelectDateWidget
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from import_export.forms import ImportForm, ConfirmImportForm
from django.forms.widgets import PasswordInput, TextInput, Select, NumberInput
from .widgets import XDSoftDateTimePickerInput





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
    username=forms.CharField(widget=TextInput(attrs={
        'class':'form-input',
        'placeholder' : 'Email',
        'type' : 'text'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password'}))


class CreateEventForm(ModelForm):

    class Meta:
        model = Event
        fields = ['title', 'location', 'price', 'maxTix']
        exclude = ['status']


class DateForm(forms.Form): 
    date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%'], 
        widget=XDSoftDateTimePickerInput()
    )


       
    


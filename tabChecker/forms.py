from django import forms
from django.forms import ModelForm
from .models import *
from .helpers import AttendeeData
from django.utils.translation import gettext_lazy as _


class EventForm(ModelForm):
    class Meta:
        model = event
        fields = '__all__'


class MemberSheetUploadForm(forms.ModelForm):
    class Meta:
        model = MemberSheetUpload
        fields = ('description', 'document', )


import os

from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django import forms

from django.utils.translation import ngettext
from .models import *
import qrcode
from PIL import Image
from .views import QRmaker
from .forms import *
from django.conf import settings
import requests
import json
from time import sleep
from django.core import mail
from django.core.mail import EmailMessage
from .helpers import *
from import_export import resources
from import_export.admin import ImportMixin, ImportExportModelAdmin, ImportForm, ConfirmImportForm
from .resources import MemberResource
import tablib
import pandas as pd


# Register your models here.

class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ['email', 'first_name', 'last_name']
    list_filter = ('email', 'first_name', 'last_name', 'is_active', 'is_staff',)
    list_display = ('email', 'first_name', 'last_name',
                    'is_active', 'is_staff')
    ordering = ('email',)

def getOrgIds(qs):
    orgIds = []
    for i in range(len(qs)):
        z = qs[i].get('AttendingOrgs')
        orgIds.append(z)

    return orgIds

def getOrgMembersById(orgIds):
    qs = []
    print(orgIds)
    for i in range(len(orgIds)):
        filtered = Members.objects.all().filter(organization=orgIds[i])
        for f in range(len(filtered)):
            qs.append(filtered[f].id)

        print(filtered)
    print(qs)
    return qs

def getEmailByMemberIDs(memIds):
    emails = []
    for i in range(len(memIds)):
        emails.append(Members.objects.get(pk=memIds[i]).email)

    print(emails)
    return emails

def getPhonesByMemberIDs(memIds):
    nums = []
    for i in range(len(memIds)):
        nums.append(Members.objects.get(pk=memIds[i]).phone)


def getCarrierEXT(number):
    carrierMatchwExtensions = {
        'CELLCO PARTNERSHIP DBA VERIZON': '@vzwpix.com',
        'NEW CINGULAR WIRELESS PCS, LLC': '@mms.att.net',
        'T-MOBILE USA, INC.': '@tmomail.com',
        'POWERTEL ATLANTA LICENSES, INC': '@tmomail.com'
    }

    url = 'https://api.telnyx.com/v1/phone_number/1' + number
    print(url)
    html = requests.get(url, headers={'User-agent': 'PalomaParkBot'})
    print(html)

    sleep(1)

    data = json.loads(html.text)

    html.close()
    carrier = data["carrier"]["name"]
    print(carrier)

    return carrierMatchwExtensions[carrier]


def getAttendeesPhonesAsEmails(queryset):
    numbers = []
    qs = queryset.get().attendees.values('phone')
    for i in range(len(qs)):
        numbers.append(qs[i].get('phone')[2:])

    for i in range(len(numbers)):
        print(numbers[i])
        ext = getCarrierEXT(numbers[i])

        numbers[i] = numbers[i] + ext

    return numbers


def getAttendeeName(queryset):
    print(queryset.get().attendees)
    fN = queryset.get().attendees.first_name
    lN = queryset.get().attendees.last_name

    return f'{fN} {lN}'


@admin.action(description='Generate Custom QR code')
def generateAndPushQR(self, request, queryset):
    qs = queryset.all().values('AttendingOrgs')
    print(qs)
    orgIds = getOrgIds(qs)
    memIds = getOrgMembersById(orgIds)

    QRimg = QRmaker(queryset)
    MemberEmails = getEmailByMemberIDs(memIds)
    print(MemberEmails)

    def getOrgs():
        t = f'{Organization.objects.get(pk=orgIds[0])} and '
        for org in range(len(orgIds) - 1):
            t += f'{Organization.objects.get(pk=orgIds[org+1])}'
        return t

    eventTitle = f' {getOrgs()} {queryset.get().title} at {queryset.get().location.name}'
    print(MemberEmails)
    #print(AttendeesPhoneEmails)
    repList = MemberEmails
    barName = queryset.get().location.name

    QRimg.save(f'{barName}_QR.png')
    for i in range(len(repList)):
        email = EmailMessage(
            f'Here are your tickets for the {eventTitle}',
            f'Thank you again {Members.objects.filter(email=repList[i]).get()} for your purchase please present '
            'the attached qr code to the employees at the entrance',
            to=[repList[i]],
            reply_to=['DEFAULT_FROM_EMAIL']
        )

        email.attach_file(f'{barName}_QR.png')

        print(email)
        if email.send():
            print('sent')







class BarAdmin(admin.ModelAdmin):
    list_display = ['name']


class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'Attending_Orgs']

    def Attending_Orgs(self, obj):
        return "\n , ".join([p.name for p in obj.AttendingOrgs.all()])

    actions = [generateAndPushQR]


class CustomMemberAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = MemberResource
    list_display = ('id', 'first_name', 'last_name', 'organization', 'email', 'phone')

    def get_import_form(self):
        return CustomImportForm

    def get_confirm_import_form(self):
        return CustomConfirmImportForm

    def get_form_kwargs(self, form, *args, **kwargs):
        # pass on `author` to the kwargs for the custom confirm form
        if isinstance(form, CustomImportForm):
            if form.is_valid():
                organization = form.cleaned_data['organization']

                kwargs.update({'organization': organization.id})
                print(kwargs.get('import_file_name'))
                FileName = kwargs.get('import_file_name')
                print(kwargs.get('organization'))

                dSet = pd.read_csv(FileName)
                print(dSet)
                for d in dSet.index:
                    dSet.at[d, 'organization'] = str(kwargs.get('organization'))
                print(dSet)
                adjusted = dSet.to_csv(f'{FileName}', index=False)
                print(adjusted)
                print(type(adjusted))

        return kwargs


admin.site.register(User, UserAdminConfig)
admin.site.register(bar, BarAdmin)
admin.site.register(Manager)
admin.site.register(Members, CustomMemberAdmin)
admin.site.register(Organizer)
admin.site.register(Organization)
admin.site.register(event, EventAdmin)
admin.site.register(MemberSheetUpload)

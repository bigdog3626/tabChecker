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

    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name', 'address')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'first_name', 'last_name', 'password1', 'is_active', 'is_staff')}

         ),

        ('Permissions', {'fields':('groups',)}),

    )



""" def getEmailNumberByMemberIDs(memIds):
    emails = {}
    for i in range(len(memIds)):
        emails[i] = list(
            Members.objects.filter(pk=memIds[i]).values_list('id', 'first_name', 'last_name', 'email', 'phone')[0])
    for z in range(len(emails)):
        emails[z][4] += getCarrierEXT(emails[z][4][2:])

    print('\n')
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
        ext = getCarrierEXT(numbers[i])

        numbers[i] = numbers[i] + ext

    return numbers


def getAttendeeName(queryset):
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
    MemberEmails = getEmailNumberByMemberIDs(memIds)

    def getOrgs():
        temp = ''
        print(orgIds)
        for org in orgIds:
            if org == orgIds[-1]:
                temp += f'{Organization.objects.get(pk=org)}'
            else:
                temp += f'{Organization.objects.get(pk=org)} and '
        return temp

    eventTitle = f'{getOrgs()} {queryset.get().title} at {queryset.get().location.name}'
    print(eventTitle)
    print('\n\n\n\n\n')
    print(MemberEmails)
    print('\n\n\n\n\n')
    # print(AttendeesPhoneEmails)
    repList = MemberEmails
    print('\n\n\n\n\n')
    print(repList)
    print('\n\n\n\n\n')
    barName = queryset.get().location.name
    subject = f'Here are your tickets for the {eventTitle}'

    QRimg.save(f'{barName}_QR.png')

    def EmailBody(key):
        return f'Thank you again {Members.objects.get(pk = repList[key][0])} for your purchase please present \n' \
               'the attached qr code to the employees at the entrance'

    for i in range(len(repList)):
        email = EmailMessage(
            subject,
            EmailBody(i),
            bcc=[repList[i][3], repList[i][4][2:]],
            reply_to=['DEFAULT_FROM_EMAIL']
        )

        email.attach_file(f'{barName}_QR.png')

        print(email)
        if email.send():
            print('sent')
"""

class BarAdmin(admin.ModelAdmin):
    list_display = ['name']


class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'location']

    #def Attending_Orgs(self, obj):
    #    return "\n , ".join([p.name for p in obj.AttendingOrgs.all()])

   # actions = [generateAndPushQR]


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
admin.site.register(Event, EventAdmin)
admin.site.register(MemberSheetUpload)

from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin

from django.utils.translation import ngettext
from .models import *
import qrcode
from PIL import Image
from .views import QRmaker

from django.conf import settings
import requests
import json
from time import sleep
from django.core import mail
from django.core.mail import EmailMessage
from .helpers import *


# Register your models here.

class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ['email', 'first_name', 'last_name']
    list_filter = ('email', 'first_name', 'last_name', 'is_active', 'is_staff',)
    list_display = ('email', 'first_name', 'last_name',
                    'is_active', 'is_staff')
    ordering = ('email',)


def getAttendeesEmail(queryset):
    l = []
    qs = queryset.get().attendees.values('email')
    for i in range(len(qs)):
        l.append(qs[i].get('email'))

    return l


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
    QRimg = QRmaker(queryset)
    AttendeesEmails = getAttendeesEmail(queryset)
    AttendeesPhoneEmails = getAttendeesPhonesAsEmails(queryset)
    eventTitle = f'{queryset.get().title} at {queryset.get().location.name}'
    print(AttendeesEmails)
    print(AttendeesPhoneEmails)
    repList = AttendeesEmails
    barName = queryset.get().location.name
    QRimg.save(f'{barName}_QR.png')

    email = EmailMessage(
        f'Here are your tickets for the {eventTitle}',
        f'Thank you again dearly for your purchase please present '
        'the attached qr code to the employees at the entrance',
        bcc=repList,
        reply_to=['DEFAULT_FROM_EMAIL']
    )
    email.attach_file(f'{barName}_QR.png')

    print(email)
    if email.send():
        print('sent')


@admin.action(description='Generate attendees from file')
def generateAttendees(self, request, queryset):
    a = queryset.values()[0].get('file')
    print(type(a))
    fileParse = AttendeeData(a)
    print(type(fileParse.parsed))
    print(len(fileParse.parsed))
    print(fileParse.userInfoDict(0))

    for i in range(len(fileParse.parsed)):
        Attendee.objects.create(
            first_name=fileParse.userInfoDict(i).get('First Name'),
            last_name=fileParse.userInfoDict(i).get('Last Name'),
            phone = f"+1{fileParse.userInfoDict(i).get('Phonenumber')}",
            email = fileParse.userInfoDict(i).get('Email')
        )


class AttendeesUpload(admin.ModelAdmin):
    actions = [generateAttendees]


class BarAdmin(admin.ModelAdmin):
    list_display = ['name']


class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'location']
    actions = [generateAndPushQR]

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['OrganizationName', 'Organizer_id']

admin.site.register(User, UserAdminConfig)
admin.site.register(bar, BarAdmin)
admin.site.register(Manager)
admin.site.register(Members, AttendeesUpload)
admin.site.register(Organizer)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(event, EventAdmin)
admin.site.register(MemberSheetUpload)

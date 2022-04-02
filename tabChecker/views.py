from django.shortcuts import render, redirect
from .models import *
from PIL import Image
import qrcode
from django.forms import formset_factory
from django.shortcuts import render
from .forms import EventForm, MemberSheetUploadForm
from django.http import HttpResponseRedirect

# Create your views here.

from django.utils import timezone
from django.views.generic.list import ListView

from .models import event


def QRmaker(queryset):
    qs = queryset.values('location')[0]
    Logo_link = bar.objects.get(pk=qs.get('location')).logo

    print(type(Logo_link))
    print(Logo_link)
    logo = Image.open(Logo_link)
    basewidth = 100
    wpercent = (basewidth / float(logo.size[0]))
    hsize = int((float(logo.size[1]) * float(wpercent)))
    logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
    QRcode = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )
    url = bar.objects.get(pk=qs.get('location')).website
    QRcode.add_data(url)
    QRcode.make()
    QRcolor = 'Grey'
    QRimg = QRcode.make_image(
        fill_color=QRcolor, black_color='white').convert('RGB')
    pos = ((QRimg.size[0] - logo.size[0]) // 2,
           (QRimg.size[1] - logo.size[1]) // 2)
    QRimg.paste(logo, pos)

    return QRimg


def manage_events(request):
    EventFormSet = formset_factory(EventForm)
    if request.method == 'POST':
        formset = EventFormSet(request.POST, request.FILES)
        if formset.is_valid():
            # do something with the formset.cleaned_data
            for form in formset:
                form.save()
            pass
    else:
        formset = EventFormSet()
    return render(request, 'tabChecker/manage_events.html', {'formset': formset})


def model_form_upload(request):
    if request.method == 'POST':
        f = MemberSheetUploadForm(request.POST, request.FILES)
        if f.is_valid():
            f.save()
            return redirect('home')
        else:
            form = MemberSheetUploadForm()
        return render(request, 'tabChecker/model_form_upload.html', {
            'form': form
        })


def home(request):
    documents = model_form_upload.objects.all()
    return render(request, 'tabChecker/home.html', {'documents': documents})

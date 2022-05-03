from django.http import HttpResponseRedirect
from PIL import Image
import qrcode
from .forms import MemberSheetUploadForm, CreateEventForm, DateForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate  # add this
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomAuthenticationForm
from django.views.generic.base import TemplateView
from django.contrib.admin.views.decorators import staff_member_required
import stripe
from .serializers import EventSerializer
from rest_framework import generics




from .forms import CreateEventForm, MemberSheetUploadForm

from .models import *


# Create your views here.


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




def register_request(request):
    pass


def login_request(request):
    if request.method == "POST":
        form = CustomAuthenticationForm
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("main:homepage")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = CustomAuthenticationForm
    return render(request=request, template_name="tabChecker/login.html", context={"login_form": form})


class HomePageView(TemplateView):
    template_name='tabChecker/home.html'
    pass


def createEvent(request): 
    if request.method=="POST":
        f = CreateEventForm(request.POST)
        g = DateForm(request.POST)
        if f.is_valid():
            return HttpResponseRedirect('tabChecker/login.html')
    else:
        f = CreateEventForm
        g = DateForm
    return render(request, 'tabChecker/createEvent.html', {'f' : f , 'g' : g})

class manageVenue(TemplateView):
    template_name='tabChecker/manageVenue.html'
    pass



class EventListView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer



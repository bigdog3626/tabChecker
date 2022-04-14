from .models import *
from PIL import Image
import qrcode
from django.forms import formset_factory
from .forms import EventForm, MemberSheetUploadForm
import qrcode
from PIL import Image
from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate  # add this
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomAuthenticationForm



from .forms import EventForm, MemberSheetUploadForm
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

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import MemberSheetUploadForm, login_request, HomePageView, createEvent, manageVenue



urlpatterns = [

    path('model_form_upload', MemberSheetUploadForm, name='upload'),
    path('login/', login_request, name='login'),
    path('', HomePageView.as_view(), name='home'),
    path('createEvent', createEvent, name="createEvent"),
    path('Manage', manageVenue.as_view(), name="manage" )

]
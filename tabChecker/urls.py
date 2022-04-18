from django.urls import path
from django.contrib.auth import views as auth_views
from .views import manage_events, MemberSheetUploadForm, login_request, HomePageView



urlpatterns = [
    path('manage_events', manage_events, name='manage_events'),
    path('model_form_upload', MemberSheetUploadForm, name='upload'),
    path('login/', login_request, name='login'),
    path('home', HomePageView.as_view(), name='home')

]
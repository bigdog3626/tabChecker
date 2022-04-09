from django.urls import path
from django.contrib.auth import views as auth_views
from .views import manage_events, MemberSheetUploadForm, login_request
app_name = 'tabChecker'

urlpatterns = [
    path('manage_events', manage_events, name='manage_events'),
    path('model_form_upload', MemberSheetUploadForm, name='upload'),
    path('login/', login_request, name='login'),

]
from django.urls import path

from .views import manage_events, MemberSheetUploadForm
app_name = 'tabChecker'

urlpatterns = [
    path('manage_events', manage_events, name='manage_events'),
    path('model_form_upload', MemberSheetUploadForm, name='upload')
]
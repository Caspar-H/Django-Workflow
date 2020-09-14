from django.urls import path

from wfautomation import views

app_name = 'wfautomation'
urlpatterns = [
    path('pdf_extraction/', views.pdf_extraction, name='pdf_extraction'),
    path('generate_site_survey_report/', views.generate_site_survey_report, name='generate_site_survey_report'),
    path('generate_site_survey_report2/<str:task_name>/<str:site_id>/<str:ins_id>', views.generate_site_survey_report2,
         name='generate_site_survey_report2'),
    path('define_poi/<str:task_name>/<str:site_id>/<str:ins_id>', views.POICreateView.as_view(), name='define_poi'),
    path('upload_site_survey/<str:task_name>/<str:site_id>/<str:ins_id>', views.upload_site_survey, name='upload_site_survey'),
]

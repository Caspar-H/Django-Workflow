from django.urls import path

from wfautomation import views

app_name = 'wfautomation'
urlpatterns = [
    path('pdf_extraction/', views.pdf_extraction, name='pdf_extraction'),
    path('generate_site_survey_report/', views.generate_site_survey_report, name='generate_site_survey_report'),
]
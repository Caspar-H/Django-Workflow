from django.urls import path

from fileupload import views

app_name = 'fileupload'

urlpatterns = [
    path('documents_folder/', views.documents_folder, name='documents_folder'),
    path('documents_folder_v2/', views.documents_folder_v2, name='documents_folder_v2'),
    path('documents_download/', views.documents_download, name='documents_download'),
    # path('documents_download_v2/', views.documents_download_v2, name='documents_download_v2'),

    path('documents_upload/', views.documents_upload, name='documents_upload'),
    # path('documents_upload_v2/', views.documents_upload_v2, name='documents_upload_v2'),
]
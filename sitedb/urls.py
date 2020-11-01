from django.urls import path

from sitedb import views

app_name = 'sitedb'
urlpatterns = [
    path('load_site_data/', views.load_site_data, name='load_site_data'),
    path('init_site_status/', views.init_site_status, name='init_site_status'),
    path('delete_site_data/', views.delete_site_data, name='delete_site_data'),

    path('home/', views.home, name='home'),

    path('site_list/', views.SiteListView.as_view(), name='site_list'),
    path('site_detail_info/<str:site_id>', views.SiteDetailView.as_view(), name='site_detail_info'),
    path('site_update_info/<str:site_id>', views.SiteUpdateView.as_view(), name='site_update_info'),
    path('site_log_list/<str:site_id>', views.SiteLogListView.as_view(), name='site_log_list'),
    path('user_log_list/', views.UserLogListView.as_view(), name='user_log_list'),

    path('milestone_overview/', views.milestone_overview, name='milestone_overview'),
    path('milestone_detail/<str:milestone_name>/', views.milestone_detail, name='milestone_detail'),

    path('milestone/<str:task_name>/<str:site_id>', views.milestone_task, name='milestone_task'),
    path('claim/<str:task_name>/<str:site_id>/<str:ins_id>', views.claim_task, name='claim_task'),
    path('unclaim/<str:task_name>/<str:site_id>/<str:ins_id>', views.unclaim_task, name='unclaim_task'),
    path('complete/<str:task_name>/<str:site_id>/<str:ins_id>', views.complete_task, name='complete_task'),
    path('complete_gateway/<str:task_name>/<str:site_id>/<str:ins_id>', views.complete_gateway_task,
         name='complete_gateway_task'),
    path('assign/<str:task_name>/<str:site_id>/<str:ins_id>', views.assign_task, name='assign_task'),

    path('my_task/', views.my_task, name='my_task'),
    path('my_group_task/', views.my_group_task, name='my_group_task'),

    # project based site table
    path('site_list_activation/', views.ActivationListView.as_view(), name='site_list_activation'),
    path('load_site_data_activation/', views.load_site_data_activation, name='load_site_data_activation'),

    path('site_list_swap/', views.SwapListView.as_view(), name='site_list_swap'),
    path('load_site_data_swap/', views.load_site_data_swap, name='load_site_data_swap'),

    # individual tasks / POI, Documents Upload, and Generate Report
    # path('task_poi/<str:site_id>', views.task_poi, name='task_poi'),
    # path('task_documents_upload/<str:site_id>', views.task_documents_upload, name='task_documents_upload'),
    # path('task_generate_report/<str:site_id>', views.task_generate_report, name='task_generate_report'),

]

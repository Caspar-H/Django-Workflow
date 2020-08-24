from django.urls import path

from sitedb import views

app_name = 'sitedb'
urlpatterns = [
    path('load_site_data/', views.load_site_data, name='load_site_data'),
    path('init_site_status/', views.init_site_status, name='init_site_status'),

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

]

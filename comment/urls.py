from django.urls import path

from comment import views


app_name = 'comment'
urlpatterns = [
    path('post_comment/<str:site_id>/', views.post_comment, name='post_comment'),
    path('notice_list/', views.CommentNoticeListView.as_view(), name='notice_list'),
    path('notice_update/', views.CommentNoticeUpdateView.as_view(), name='notice_update'),
]

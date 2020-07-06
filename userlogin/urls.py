from django.urls import path, include

from userlogin import views

app_name = 'userlogin'

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.SignUpView.as_view(), name='signup'),
    path('accounts/signup/rf/', views.RFSignUpView.as_view(), name='rf_signup'),
    path('accounts/signup/eme/', views.EMESignUpView.as_view(), name='eme_signup'),
    path('accounts/signup/manager/', views.ManagerSignUpView.as_view(), name='manager_signup'),

    path('profile_edit/<int:id>/', views.profile_edit, name='profile_edit'),
    path('setting_edit/<int:id>/', views.setting_edit, name='setting_edit'),

]

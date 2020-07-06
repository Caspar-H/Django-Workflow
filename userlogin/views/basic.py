from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from userlogin.forms import UserProfileForm, UserSettingForm
from userlogin.models import User, UserSetting


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def profile_edit(request, id):
    user = User.objects.get(id=id)
    # profile = Profile.objects.get(id=id)

    if request.method == 'POST':
        if request.user != user:
            return HttpResponse("Permission Denied")

        user_form = UserProfileForm(request.POST)
        if user_form.is_valid():
            user_cd = user_form.cleaned_data
            user.first_name = user_cd['first_name']
            user.last_name = user_cd['last_name']
            user.email = user_cd['email']

            # if 'avatar' in request.FILES:
            #     profile.avatar = profile_cd['avatar']
            user.save()

            return redirect('userlogin:profile_edit', id=id)
        else:
            return HttpResponse("Form info incorrect")
    elif request.method == "GET":
        profile_form = UserProfileForm(initial={'first_name': user.first_name,
                                                'last_name': user.last_name,
                                                'email': user.email})

        context = {
            'profile_form': profile_form,
            'user': user,
        }
        return render(request, 'registration/profile_edit.html', context)
    else:
        return HttpResponse("POST or GET request only")


def setting_edit(request, id):
    user = User.objects.get(id=id)

    if UserSetting.objects.filter(user_id=id).exists():
        user_setting = UserSetting.objects.get(user_id=id)
    else:
        user_setting = UserSetting.objects.create(user=user)

    if request.method == 'POST':
        if request.user != user:
            return HttpResponse("Permission Denied")

        setting_form = UserSettingForm(request.POST)
        if setting_form.is_valid():
            user_cd = setting_form.cleaned_data
            user_setting.email_notification = user_cd['email_notification']

            user_setting.save()

            return redirect('userlogin:setting_edit', id=id)
        else:
            return HttpResponse("Form info incorrect")
    elif request.method == "GET":
        setting_form = UserSettingForm(initial={'email_notification': user_setting.email_notification,})

        context = {
            'setting_form': setting_form,
            'user': user,
        }
        return render(request, 'registration/setting_edit.html', context)
    else:
        return HttpResponse("POST or GET request only")
